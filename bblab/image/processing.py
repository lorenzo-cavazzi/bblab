"""
This module contains functions to analyze single channel images from microscopes.
"""
import os
import logging
import numpy
import cv2
import csv
from pathlib import Path

# TODO: Logging should be implemented at module level. It has temporary been added
# to already use logging properly while writing the first release
log = logging.getLogger("bblab")


def set_log_level(level = logging.WARNING):
    """Define log level. Please consider this solution as temporary.

     Args:
        level (int): loggging level. Please use logging.DEBUG .INFO .WARNING
            .ERROR .CRITICAL from the `logging` module.
    """
    log.setLevel(level)

def overlay_channels(input_folder = None, output_folder = None, return_image = False,
        maximize_intensity = False, **kwargs):
    """Overlay 3 single channel Tiff images in a RGB image. The finaly image may be
    returned as a numpy array and/or saved as a Png file.
    Input images are supposed to be 8 or 16 bit single channel scans from a microscope.
   
    Args:
        input_folder (str): folder path containing the 3 input Tiff images. If None,
            the current folder is used.
            This parameter is ignored when `input_files` is provided.
        output_folder (str): folder path where output image will be saved. If None, the
            current folder is used. If False, output won't be saved (useful when
            `return_image` is True).
            This parameter is ignored when `output_file` is provided.
        return_image (bool): defines if image is returned. Can't be False if an output
            file or folder is not provided.
        maximize_intensity (bool) : defines if each channell intensity must use all
            the available depth. The ratio will be preserved for each channel, but not
            between them. Please use the `x_channel_multiplier` variables to further
            adjust each single channel intensity.
        **input_files (:obj:`list` of :obj:`str`): list of Tiff images paths
        **output_file (str): output image path. If it doesn't end with .png, the
            extension will be added.
        **r_channel_multiplier (float): red channel intensity multiplier. If
            `maximize_intensity` is True, this will be applied after that transformation.
        **g_channel_multiplier (float): green channel intensity multiplier. If
            `maximize_intensity` is True, this will be applied after that transformation.
        **b_channel_multiplier (float): blue channel intensity multiplier. If
            `maximize_intensity` is True, this will be applied after that transformation.
    
    Returns:
        if `return_image` is True, it returns the numpy array representing the overlayed
            image.

    Examples:
        Overlay images from input folder, save the result in output folder

        >>> overlay_channels("data/channels/", "output/overlay/")

        Overlay images from specific paths, output result as a numpy array

        >>> overlay_channels(input_files=["r.tiff", "g.tiff", "b.tiff"],
            return_image=False, maximize_intensity=True)
        array([[[    0,    34,   347],
        [    0,     0,    59],
        [    0,     0,   167],
        ...,
        ...,
        [13480,    11,  6736],
        [ 8295,    23,  5622],
        [  622,     0,   419]]], dtype=uint16)

        Read and write in current folder, enhance specific channels

        >>> overlay_channels(r_channel_multiplier = 0.5, b_channel_multiplier = 5)
	"""

    # check input files
    if "input_files" in kwargs:
        files = _get_validated_filenames(kwargs["input_files"])
    else:
        if input_folder is None:
            input_folder = "."
        files = _get_filenames_from_folder(input_folder)
        files.sort() # let's make RGB association deterministic for equal sets of names
    if len(files) != 3:
        raise ValueError("3 files expected, {num} found".format(num=str(len(files))))
    extensions = set([file.suffix for file in files])
    # TODO: the following is NOT a good way to test file format. A Tiff image may not have
    # .tiff suffix, an a .tiff suffix doesn't mean file is a Tiff image. This is a
    # simplification but it also enforce to use proper file extensions
    if ".tiff" not in extensions or len(extensions) > 1:
        raise ValueError("only .tiff files are accepted")
    log.info("working on the following input files: {names}".format(names=[str(file.absolute()) for file in files]))

    # get files, apply transformations (where needed) and create RGB image
    channels = []
    for file in files:
        channel = cv2.imread(str(file), cv2.IMREAD_UNCHANGED)
        if maximize_intensity:
            channel_type = numpy.iinfo(channel.dtype)
            # TODO: better using a threshold? like
            # image_type.max(image) - image_type.max(image)/100
            if numpy.max(channel) < channel_type.max:
                channel = channel.astype(numpy.float64)
                channel *= channel_type.max / numpy.max(channel)
                channel = channel.astype(channel_type)
        channels.append(channel)
    # remember that opencv precess data as BGR instead of RGB...
    if maximize_intensity:
        loginfo = ["channels intensity has been maximized"]
    else:
        loginfo = ["original channels intensity"]
    # TODO: 3 similar repetitions are enought to loop or create a function
    if "b_channel_multiplier" in kwargs:
        channels[0] *= kwargs["b_channel_multiplier"]
        if numpy.max(channels[0]) > numpy.iinfo(channels[0].dtype).max:
            log.warning("blue channel values are higher than channel depth. Information may be lost")
        loginfo.append("blue channel multiplied by {num}".format(num = str(kwargs["b_channel_multiplier"])))
    if "g_channel_multiplier" in kwargs:
        channels[1] *= kwargs["g_channel_multiplier"]
        if numpy.max(channels[1]) > numpy.iinfo(channels[1].dtype).max:
            log.warning("green channel values are higher than channel depth. Information may be lost")
        loginfo.append("green channel multiplied by {num}".format(num = str(kwargs["g_channel_multiplier"])))
    if "r_channel_multiplier" in kwargs:
        channels[2] *= kwargs["r_channel_multiplier"]
        if numpy.max(channels[2]) > numpy.iinfo(channels[2].dtype).max:
            log.warning("red channel values are higher than channel depth. Information may be lost")
        loginfo.append("red channel multiplied by {num}".format(num = str(kwargs["r_channel_multiplier"])))
    overlay_image = cv2.merge(channels)
    log.info(", ".join(loginfo))

    # save and/or return rgb_image
    if "output_file" in kwargs:
        overlay_file = _validate_filename(kwargs["output_file"], ".png")
    elif output_folder is not False:
        if (output_folder is None):
            output_folder = "."
        overlay_file = _build_validated_filename(output_folder, "overlay.png")
    else:
        overlay_file = None
    if overlay_file is not None:
        cv2.imwrite(str(overlay_file), overlay_image)
        log.info("writing file '{file}'".format(file = str(overlay_file)))
    if return_image:
        return overlay_image

def highlight_cells(input_folder_rgb = None, input_folder_mask = None,
        output_folder = None, return_image = False, cells_highlight = 0, **kwargs):
    """Highlight single cells from a Png RGB image and a Tiff single channel mask.
	The finaly image may be returned as a numpy array and/or saved as a Png file.
    Input Png is supposed to be a 24 or 48 bits RGB image, input Tiff a 8 or 16 bit
	single channel segmentation mask.

    Args:
        input_folder_rgb (str): folder path containing the input Png RGB image.
            If None, the current folder is used.
            This parameter is ignored when `input_file_rgb` or `input_data_rgb`
            is provided.
        input_folder_mask (str): folder path containing the input Tiff mask image.
            If None, the current folder is used.
            This parameter is ignored when `input_file_mask` or `input_data_mask`
            is provided.
        output_folder (str): folder path where output image will be saved. If None, the
            current folder is used. If False, output won't be saved (useful when
            `return_image` is True).
            This parameter is ignored when `output_file` is provided.
        return_image (bool): defines if image is returned. Can't be False if an output
            file or folder is not provided.
        cells_highlight (int): defines the highlighting method.
            0 (default): apply the mask as transparency layer. All information from the
            mask is preserved, but image may be almost all trasparent.
            1 (opaque cells): cells are identified from mask and made opaque. All
            information about single cells is lost.
            2 (emphasize cells): the transparency mask is modified to try to make
            cells as opaque as possible without losing the information that
            distinguish single cells. Cell ids are changed in the process, but
            image may appear much better.
        **input_file_rgb (str): input Png RGB image path. This parameter is ignored
            when `input_data_rgb` is provided.
        **input_data_rgb: numpy array with the Png RGB image data.
        **input_file_mask (str): input Tiff mask image path. This parameter is ignored
            when `input_data_mask` is provided.
        **input_data_mask: numpy array with the Tiff mask image data.
        **output_file (str): output image path. If it doesn't end with .png, the
            extension will be added.

    Returns:
        if `return_image` is True, it returns the numpy array representing the overlayed
            image.

    Examples:
        # Get images from specific input folders, save the result in output folder

        >>> highlight_cells("output/mask/", "data/overlay/", "output/highlight/")

        Get images from paths, output result as a numpy array

        >>> highlight_cells(input_file_rgb="overlay_rgb.png",
            input_data_rgb="mask.tiff", output_folder=False, return_image=True)
        array([[[    0,    34,   347,     0],
        [    0,     0,    59,     0],
        [    0,     0,   167,     0],
        ...,
        ...,
        [13480,    11,  6736,     0],
        [ 8295,    23,  5622,     0],
        [  622,     0,   419,     0]]], dtype=uint16)

        Read and write in current folder, change cell highlight method

        >>> overlay_channels(cell_highlight = 2)
	"""

    # get input images
    rgb_image = None
    if "input_data_rgb" in kwargs:
        rgb_image = kwargs["input_data_rgb"]
    elif "input_file_rgb" in kwargs:
        rgb_files = _get_validated_filenames(kwargs["input_file_rgb"])
    else:
        if input_folder_rgb is None:
            input_folder_rgb = "."
        rgb_files = _get_filenames_from_folder(input_folder_rgb)
    if rgb_image is None:
        if len(rgb_files) != 1:
            raise ValueError("1 rgb file expected, {num} found".format(num=str(len(rgb_files))))
        if rgb_files[0].suffix != ".png":
            raise ValueError("only .png extension is accepted")
        log.info("working on the following rgb file: {name}".format(name=str(rgb_files[0].absolute())))
        rgb_image = cv2.imread(str(rgb_files[0]), cv2.IMREAD_UNCHANGED)
    mask_image = None
    if "input_data_mask" in kwargs:
        mask_image = kwargs["input_data_mask"]
    elif "input_data_rgb" in kwargs:
        mask_files = _get_validated_filenames(kwargs["input_data_rgb"])
    else:
        if input_folder_mask is None:
            input_folder_mask = "."
        mask_files = _get_filenames_from_folder(input_folder_mask)
    if mask_image is None:
        if len(mask_files) != 1:
            raise ValueError("1 Tiff mask expected, {num} found".format(num=str(len(mask_files))))
        if mask_files[0].suffix != ".tiff":
            raise ValueError("only .tiff extension is accepted")
        log.info("working on the following mask file: {name}".format(name=str(mask_files[0].absolute())))
        mask_image = cv2.imread(str(mask_files[0]), cv2.IMREAD_UNCHANGED)

    # compute transparency channel from mask
    log_info = "mask channel identifies {num} different cells".format(num=str(len(numpy.unique(mask_image)) - 1))
    if cells_highlight == 2:
        # the idea is to highlight cells as much as possible, preserving the possibility
        # to distinguish them looking the transparency channel
        log_info += "; cells highlighting algorithm will modify cell_id information stored in the transparency channel"
        mask_type = numpy.iinfo(mask_image.dtype)
        if numpy.max(mask_image) < mask_type.max:
            channel_a = mask_type.max + 1 - mask_image
            channel_a[channel_a > mask_type.max] = 0
            channel_a = channel_a.astype(mask_type)
    elif cells_highlight == 1:
        log_info += "; cells highlighting algorithm will remove cell_id information from transparency channel"
        channel_a = numpy.copy(mask_image)
        channel_a[channel_a > 0] = mask_type.max
    else:
        channel_a = mask_image
    log.info(log_info)

    # create RGBA image, save and/or return it
    channel_b, channel_g, channel_r = cv2.split(rgb_image)
    highlight_image = cv2.merge((channel_b, channel_g, channel_r, channel_a))
    if "output_file" in kwargs:
        highlight_file = _validate_filename(kwargs["output_file"], ".png")
    elif output_folder is not False:
        if (output_folder is None):
            output_folder = "."
        highlight_file = _build_validated_filename(output_folder, "highlight.png")
    else:
        highlight_file = None
    if highlight_file is not None:
        cv2.imwrite(str(highlight_file), highlight_image)
        log.info("writing file '{file}'".format(file = str(highlight_file)))
    if return_image:
        return highlight_image

def compute_mean(input_folder = None, output_folder = None, return_data = False,
        **kwargs):
    """Computes the mean of each color channel for every cell identified by the
    transparency channel. The final table may be returned as a list of dictionaries
    or saved in a Csv file.
    Input Png is supposed to bo a 32 or 64 bits RGBA image where the transparency
    channel holds the cell id.

    Args:
        input_folder (str): folder path containing the Png RGBA image. If None,
            the current folder is used.
            This parameter is ignored when `input_file` or `input_data` is provided.
        output_folder (str): folder path where output Csv will be saved. If None, the
            current folder is used. If False, output won't be saved (useful when
            `return_data` is True).
            This parameter is ignored when `output_file` is provided.
        return_data (bool): defines if data are returned. Can't be False if an output
            file or folder is not provided.
        **input_file (str): input Png RGBA path. This parameter is ignored when
            `input_data` is provided.
        **input_data (str): numpy array with the Png RGBA image data.
        **output_file (str): output Csv path. If it doesn't end with .csv, the
            extension will be added.
        
    Returns:
        if `return_data` is True, it returns the Csv file containing R-G-B channels
        mean for every cell_id.
        
    Examples:
        Get image from specific input folders, save the data in output folder
        
        >>> compute_mean("output/highlight/", "output/mean/")

        Get images from path, output result as a list of dictionaries
        
        >>> highlight_cells(input_file_rgb="overlay_rgb.png",
    """
    
    # get input RGBA image
    rgba_image = None
    if "input_data" in kwargs:
        rgba_image = kwargs["input_data"]
    elif "input_file" in kwargs:
        rgba_files = _get_validated_filenames(kwargs["input_file"])
    else:
        if input_folder is None:
            input_folder = "."
        rgba_files = _get_filenames_from_folder(input_folder)
    if rgba_image is None:
        if len(rgba_files) != 1:
            raise ValueError("1 rgb file expected, {num} found".format(num=str(len(rgba_files))))
        if rgba_files[0].suffix != ".png":
            raise ValueError("only .png extension is accepted")
        log.info("working on the following rgba file: {name}".format(name=str(rgba_files[0].absolute())))
        rgba_image = cv2.imread(str(rgba_files[0]), cv2.IMREAD_UNCHANGED)
    
    # compute channels means
    channel_b, channel_g, channel_r, channel_a = cv2.split(rgba_image)
    cell_ids = list(numpy.unique(channel_a))
    cell_ids.sort()
    if (cell_ids[0] == 0):
        del cell_ids[0]
    cell_means = []
    for cell_id in cell_ids:
        mean_r = _get_channel_mean(channel_r, channel_a == cell_id)
        mean_g = _get_channel_mean(channel_g, channel_a == cell_id)
        mean_b = _get_channel_mean(channel_b, channel_a == cell_id)
        # cell_means.append((cell_id, mean_r, mean_g, mean_b))
        cell_means.append({ "cell_id": cell_id, "red": mean_r, "green": mean_g, "blue": mean_b})

    # save and/or return values
    if "output_file" in kwargs:
        mean_file = _validate_filename(kwargs["output_file"], ".csv")
    elif output_folder is not False:
        if (output_folder is None):
            output_folder = "."
        mean_file = _build_validated_filename(output_folder, "cell_means.csv")
    else:
        mean_file = None
    if mean_file is not None:
        keys = cell_means[0].keys()
        with open(str(mean_file), "w", newline="") as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames = keys)
            dict_writer.writeheader()
            dict_writer.writerows(cell_means)
            log.info("writing file '{file}'".format(file = str(mean_file)))
    if return_data:
        return cell_means

# Auxiliary functions to get/write data
def _get_channel_mean(channel, mask, round_decimal = 2):
    """get a numpy array n*m and a mask (bit) of the same size. Compute the mean
    of values in the array not filtered by the mask
    """
    channel_masked = channel * mask
    mean = numpy.mean(channel_masked[channel_masked > 0])
    if str(mean) == "nan":
        return 0
    return round(mean, round_decimal)

def _get_filenames_from_folder(folder):
    """get the `folder` str, checks and returns children as list of Path
    instances."""

    folder_path = Path(folder)
    if not folder_path.is_dir():
        raise ValueError("'{path}' is not a valid directory".format(path=folder))
    files = os.listdir(folder)
    if not files:
        raise ValueError("'{path}' doesn't contain any file".format(path=folder))
    return [folder_path.joinpath(file) for file in files]

def _get_validated_filenames(*args):
    """get one or more filename str or list(str), checks validity and returns
    list of Path instances."""

    files = []
    for arg in args:
        if not isinstance(arg, list):
            arg = [arg]
        for elem in arg:
            file = Path(elem)
            if not file.is_file():
                raise ValueError("'{elem}' is not a valid file".format(arg=str(arg)))
            files.append(file)
    return files

def _build_validated_filename(folder, filename, extension=None):
    """ check `folder` str validity, attach `filename` str and `extension` str
    (if provided) and returns Path instance"""

    folder_path = Path(folder)
    if not folder_path.is_dir():
        raise ValueError("'{path}' is not a valid directory".format(path=folder))
    if extension is not None and not filename.endswith(extension):
        filename += extension
    return folder_path.joinpath(filename)

def _validate_filename(filename, extension=None):
    """ check `filename` str validity, attach `extension` str (if provided)
    and returns Path instance"""

    path = Path(filename)
    print(path.parent, path.name)
    return _build_validated_filename(path.parent, path.name, extension)

