"""
This module contains functions to analyze single channel images from microscopes.
"""

# use Google notation: https://github.com/google/styleguide/blob/gh-pages/pyguide.md
# this is the alternative notation: https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard


from pathlib import Path

def overlay_channels(input_folder = None, output_folder = None, return_image = False,
        maximize_intensity = True, **kwargs):
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

    print("overlay_channels stub")
    # remember to catch errors and write some feedback to the standard output
    raise NotImplementedError


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
        **input_file_rgb (str): input Png RGB image path.
        **input_data_rgb: numpy array with the Png RGB image data.
        **input_file_mask (str): input Tiff mask image path.
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

    print("highlight_cells stub")
    raise NotImplementedError


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
            This parameter is ignored when `input_file` is provided.
        output_folder (str): folder path where output Csv will be saved. If None, the
            current folder is used. If False, output won't be saved (useful when
            `return_data` is True).
            This parameter is ignored when `output_file` is provided.
        return_data (bool): defines if data are returned. Can't be False if an output
            file or folder is not provided.
        **input_file (str): input Png RGBA path
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
    
    print("compute_mean stub")
    raise NotImplementedError