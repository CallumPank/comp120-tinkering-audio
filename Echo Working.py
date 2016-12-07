import random
import wave, struct, math


samprate = 44100
lengthwhite = 44100 * 0.5  #This is the amount of seconds
amplitude = 32767

values = []
frames = []
noise_a = wave.open('Speaking.wav', 'r')
noise_b = wave.open('noise4.wav', 'w')

length = noise_a.getnframes()
noise_b.setnchannels(1)
noise_b.setsampwidth(2)
noise_b.setframerate(samprate)
noise_b.setnframes(44100 * 100)
noise_b.setcomptype('NONE', 'not compressed')
noise_b.getparams()
frequency = 500
delay = 8000


for i in range (0, 44100):
    value = math.sin(2.0 * math.pi * frequency * (i / 44100.0)) * (0.5 * (2**15-1))
    data = struct.pack("<h", value)
    frequency += 1
    for j in range (0, 1):
        values.append(data)


for i in xrange(length):
    wave_data = noise_a.readframes(1)
    data = struct.unpack("<h", wave_data)
    frames.append(int(data[0]))


print frames
def echo(sound_file, delay):
    values = []
    channels = 1
    s1 = sound_file
    s2 = sound_file[:]
    for index in range(delay, len(s1)):
        echo = 0.6*s2[index-delay]
        s1[index] += echo
        packaged_value = struct.pack("<h", s1[index])
        for j in xrange(channels):
            values.append(packaged_value)

    print values
    value_str = ''.join(values)
    noise_b.writeframes(value_str)
    noise_b.close()
    return values

def whitenoise():
    #Creates a blank sound
    makenoise = wave.open('whitenoise.wav', 'w')
    makenoise.setparams((1, 2, 44100, lengthwhite, 'NONE', 'Not compressed'))

    for pos in range(int(length)):
        rawSample = random.uniform(-1, 1)
        sampleVal = int(amplitude * rawSample)
        packedval = struct.pack('h', sampleVal)
        makenoise.writeframes(packedval)
    return makenoise


echo(frames, 44100)
whitenoise()