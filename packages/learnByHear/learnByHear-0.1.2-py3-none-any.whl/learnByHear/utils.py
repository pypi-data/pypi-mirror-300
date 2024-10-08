import os
import fnmatch
from subprocess import run, PIPE
import ffmpeg
from tqdm import tqdm
from argostranslate import package as ATpkg
from argostranslate import translate as ATtrn

def translate(infile, outfile, outdir, from_code, to_code):
    """
    Uses Argos Translate to translate an input text file.
    Translation is done line by line.
    First translation may take some time to download.
    """
    # Download and install Argos Translate package
    ATpkg.update_package_index()
    available_pkgs = ATpkg.get_available_packages()
    pkg_to_install = next(filter(
        lambda x: x.from_code==from_code and x.to_code==to_code, available_pkgs
    ))
    ATpkg.install_from_path(pkg_to_install.download())

    # Translate and output the file
    run(["mkdir", "-p", outdir])
    out_text = ""
    with open(infile) as f:
        print("Translating: " + infile + " ...")
        totallines = sum(1 for l in f)
        f.seek(0)
        for line in tqdm(f, total=totallines):
            out_text = out_text + ATtrn.translate(line, from_code, to_code)
    with open(outdir + outfile, "w+") as f:
        f.write(out_text)

def run_piper_file(fname, outdir, model, speaker=None):
    """
    This wrapper function creates a .wav for each line in the input text file.
    Output directory will be created if it does not yet exist.
    """
    with open(fname) as f:
        run(["mkdir", "-p", outdir])
        print("Running piper-tts using: " + model)
        totallines = len([ "_" for l in f ])
        f.seek(0)
        n_line = 0
        for line in tqdm(f, total=totallines):
            n_line = n_line + 1
            p2args = ["piper", "--model", model,
                      "--output-file", outdir + str(n_line) + ".wav"]
            if speaker:
                p2args = p2args + ["--speaker", speaker]
            p2 = run(p2args, input=line, text=True, stdout=PIPE, stderr=PIPE)

def combine_audios(outputwav, out_dir, list_dirs, padding, n_repeats):
    """
    Combines the audios in each directory in the input list "list_dirs" with
         a silent padding of duration "padding" seconds and repetitions of
         1 + "n_repeats".
    The filenames of the audios must be in "i.wav" format,
        with "i" being integers starting from 1 without missing any integer.
    The number of .wav audios in each folder must be equal.
    """
    # Create silence.wav for padding audios
    (
        ffmpeg\
            .input("anullsrc=r=44100:cl=mono:d=" + str(padding),
                    format="lavfi")\
            .output(out_dir + "silence.wav", format="wav",
                    loglevel="quiet", acodec="pcm_s16le")\
            .overwrite_output()\
            .run()
    )

    # Number of .wav files in each directory
    n_wavs = []
    for d in list_dirs:
        n_wavs.append(
            len(fnmatch.filter(os.listdir(out_dir+d), '*.wav'))
        )
    try:
        assert len(set(n_wavs)) == 1
        n_wavs = n_wavs[0]
    except:
        raise RuntimeError("Number of .wav files in each dir is unequal")

    # Create a temp text file with filenames to send to ffmpeg
    txtfileout = ""
    for i in range(n_wavs):
        n = 0
        while n < n_repeats+1:
            n = n + 1
            for d in list_dirs:
                append_text =   "file '" + d + str(i+1) + ".wav'\n" + \
                                "file 'silence.wav'\n"
                txtfileout = txtfileout + append_text
    with open(out_dir + "tmp.txt", "w+") as f:
        f.write(txtfileout)

    # Concatenate audio files listed in tmp.txt and output
    (
        ffmpeg\
            .input(out_dir + 'tmp.txt', format='concat')\
            .output(out_dir + outputwav, c='copy', loglevel="quiet")\
            .overwrite_output()\
            .run()
    )
    print("\nConcatenated audios output to: " + out_dir + outputwav)



