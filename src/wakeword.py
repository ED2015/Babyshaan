import struct
import pyaudio
import pvporcupine

# Initialize Porcupine with built-in wake words ("picovoice", "bumblebee", etc.)
keyword_list=["bumblebee"]
porcupine = pvporcupine.create(access_key="V3z1pqlzVKQDQ7KWi1CmubrzbSYAqcb8eBZnVb/+huWUUrZweAzVrA==",keywords=keyword_list)

pa = pyaudio.PyAudio()

audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("Listening for wake words... (say 'bumblebee' or 'picovoice')")

try:
    while True:
        pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm_unpacked)
        
        if keyword_index >= 0:
            print(f"Wake word detected! ({keyword_list[keyword_index]})")
            # 👉 Here you can trigger your assistant’s main logic

except KeyboardInterrupt:
    print("Stopping...")

finally:
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
