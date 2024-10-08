import logging
logging.basicConfig(filename="log.txt",level=logging.DEBUG)
logging.captureWarnings(True)

from subprocess import Popen

from .utils import translate, run_piper_file, combine_audios
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="learnbyhear",
        description="Learn a new language by hearing it",
        epilog='License: GNU GPLv3.  Copyright: Dokara 2024.'
    )
    parser.add_argument('in_file', type=str,
                        help='Input text file')
    parser.add_argument('--out_dir', type=str,
                        default='tts/',
                        help='Destination for output files')
    parser.add_argument('--from_code', type=str,
                        default='en',
                        help='Input file language')
    parser.add_argument('--to_code', type=str,
                        default='de',
                        help='Output file language')
    parser.add_argument('--out_models', type=str, nargs='+',
                        default=["de_DE-thorsten-high"],
                        help='Models to use for audios of output files')
    parser.add_argument('--in_model', type=str,
                        default="en_US-lessac-high",
                        help='Model to use for audio of input file')
    parser.add_argument('--repeats', type=int,
                        default=0,
                        help='No. of repetitions in addition to one iteration')
    parser.add_argument('--padding', type=float,
                        default=0.8,
                        help='Silence padding in seconds')

    args = parser.parse_args()

    print()
    print("----------------------------")
    print("----  Learn by Hearing  ----")
    print("--    © R. Dokara 2024    --")
    print("----------------------------")
    print()

    # Parse out_dir correctly: add / if it does not exist
    if args.out_dir[-1] != '/':
        args.out_dir = args.out_dir + '/'

    # List of directories to make
    list_dirs = [str(i)+"/" for i in range(len(args.out_models)+1)]

    # Translate the input file
    translate(args.in_file, "output.txt", args.out_dir,
              args.from_code, args.to_code)

    # TTS
    run_piper_file(args.in_file,
                   args.out_dir + list_dirs[0],
                   args.in_model)
    for i, d in enumerate(list_dirs[1:]):
        run_piper_file(args.out_dir+'/output.txt',
                       args.out_dir + d,
                       args.out_models[i])

    # Combine audios
    combine_audios('output.wav', args.out_dir,
                   list_dirs, args.padding, args.repeats)

    print()
    print("---  End of Program  ---")
    print("------------------------")
    print()

if __name__ == "__main__":
    main()



