import argparse
import bblab
import sys

def main(args = sys.argv[1:]):
    desc = """bblab command line tool allows you to start bblab main functions from your shell.
    Please specify the function and its correlated parameters."""
    parser = argparse.ArgumentParser(prog="command", description=desc)
    subparsers = parser.add_subparsers(help="function to invoke. Please check function help for further details")

    def image_processing_overlay_channels():
        print("bblab.image.processing.overlay_channels")
        # bblab.image.processing.overlay_channels(input_folder=args.input_folder, output_folder=args.output_folder,
        #     maximize_intensity=args.maximize_intensity, r_channel_multiplier=args.red_multiplier,
        #     g_channel_multiplier=args.green_multiplier, b_channel_multiplier=args.blue_multiplier)
        bblab.image.processing.overlay_channels(input_folder=args.input_folder,
        output_folder=args.output_folder, maximize_intensity=args.maximize_intensity)

    def image_processing_highlight_cells():
        print("bblab.image.processing.highlight_cells")
        bblab.image.processing.highlight_cells(input_folder_rgb=args.input_folder_rgb,
            input_folder_mask = args.input_folder_mask, output_folder=args.output_folder,
            cells_highlight=args.cells_highlight)

    def image_processing_compute_mean():
        bblab.image.processing.compute_mean(input_folder=args.input_folder,
            output_folder=args.output_folder)
        print("bblab.image.processing.compute_mean")

    parser_overlay_channels_help = "overlay_channels function"
    parser_overlay_channels = subparsers.add_parser("overlay_channels", help=parser_overlay_channels_help)
    parser_overlay_channels.set_defaults(command=image_processing_overlay_channels)
    parser_overlay_channels.add_argument("-i", "--input-folder", help="folder containing Tiff single channels input files", default=".")
    parser_overlay_channels.add_argument("-o", "--output-folder", help="folder to save Png output RGB image", default=".")
    parser_overlay_channels.add_argument("-max", "--maximize-intensity", help="swith channel intensity maximization", default=False)
    #TODO: fix error in in processing.py [*=] before allowing single channel multipliers
    #parser_overlay_channels.add_argument("-r", "--red-multiplier", help="red channel intensity multiplier", default=1)
    #parser_overlay_channels.add_argument("-g", "--green-multiplier", help="green channel intensity multiplier", default=1)
    #parser_overlay_channels.add_argument("-b", "--blue-multiplier", help="blue channel intensity multiplier", default=1)
    parser_highlight_cells_help = "highlight_cells function"
    parser_highlight_cells = subparsers.add_parser("highlight_cells", help=parser_highlight_cells_help)
    parser_highlight_cells.set_defaults(command=image_processing_highlight_cells)
    parser_highlight_cells.add_argument("-irgb", "--input-folder-rgb", help="folder containing Png RGB input file", default=".")
    parser_highlight_cells.add_argument("-imask", "--input-folder-mask", help="folder containing Tiff mask file", default=".")
    parser_highlight_cells.add_argument("-o", "--output-folder", help="folder to save Png output RGBA image", default=".")
    parser_highlight_cells.add_argument("-ch", "--cells-highlight", help="define cell highlighting algorithm (0: default, 1: opaque cells, 2: emphasize cells)", default=0, type=int)
    parser_compute_mean_help = "compute_mean function"
    parser_compute_mean = subparsers.add_parser("compute_mean", help=parser_compute_mean_help)
    parser_compute_mean.set_defaults(command=image_processing_compute_mean)
    parser_compute_mean.add_argument("-i", "--input-folder", help="folder containing Png RGBA image", default=".")
    parser_compute_mean.add_argument("-o", "--output-folder", help="folder to save Csv data file", default=".")

    args = parser.parse_args()
    args.command()

if __name__ == '__main__':
    main()