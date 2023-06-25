# Audio Spitter

## Dependencies
 * ffmpeg
 
## Steps to use

### 1. Detect Silent Parts

```shell
ffmpeg -i "input.mp3" -af silencedetect=noise=-30dB:d=4 -f null - 2> report.txt
```

*Select the d parameter by trial to identify chapter endings.*

### 2. Provide Inputs in "inputs.py"

* min_silence_duration = silence duration between chapters( derived from analysis of the output file generated in the previous step)
* report_file_path = absolute path to the report.txt file generated in the previous step
* audio_file = absolute path to the mp3 file to be split
* preface_count = number of chapters before the first chapter(introduction + preface + foreword)

### 3. Run the python script

```shell
python3 functions.py
```