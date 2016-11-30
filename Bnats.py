import wave, struct, sys, math, winsound, pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 100

LENGTH_OF_TRACK = 1
SAMPLE_LENGTH = 44100 * LENGTH_OF_TRACK
FREQUENCY = float(1000)
SAMPLE_RATE = float(44100)
BIT_DEPTH = 32767           # 2 to the power (16 - 1 for sign) -1 for zero
load_file = True

volume = 0.5

values = []
new_file_frames = 132300

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
window.fill((255, 255, 255))
font = pygame.font.SysFont(None, 48)
levelText = font.render('m = mmmMMM', True, (0, 0, 0))
window.blit(levelText, (0, 0))
pygame.display.update()


class LoadSound:
    def __init__(self, name):
        """loads the file"""
        self.file = wave.open(name, "rb")

    def get_parameters(self):
        """again definitely not needed, just my train of thought"""
        self.file.getparams()

    def read_file(self):
        """returns an unpacked list of values of the sound wave"""
        unpacked_list = []
        step = BIT_DEPTH / 200  # auto tune step

        for i in xrange(self.file.getnframes()):
            current_frame = self.file.readframes(1)
            unpacked_frame = struct.unpack("<hh", current_frame)
            unpacked_list.append(unpacked_frame)

        return unpacked_list

#            unpacked_frame = step * abs(unpacked_frame[0] / step)
#            print unpacked_frame

    def write_file(self, new_file_name, values_list):
        packed_list = []
        self.file = wave.open(new_file_name, 'w')
        self.set_parameters(2, 2, 44100, 132300, 'NONE', 'not compressed')

        for i in xrange(new_file_frames):
            packed_list.append(struct.pack("<h", values_list[i]))  # [0])) , unpacked_frame[1]))

        self.file.writeframes(''.join(packed_list))
        self.file.close()

        print 'new sound made'
        """takes the list of newly created values, joins, writes to the file, then closes the wave stream"""


class CreateSound:
    """Creates a file with name 'name' """
    def __init__(self, name):
        self.file = wave.open(name, 'w')

    def set_parameters(self, nchannels, sampwidth, framerate, nframes, comptype, compname):
        """sets the parameters of the .wav file"""

        # probably unnecessary to have in a function. Just do after creating an instance
        self.file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))




def echo():

    sound_list_unpacked_to_echo = mmmMMM()
    new_list_unpacked_with_echo = []
    echo_length = 1000

    for i in xrange(0, SAMPLE_LENGTH -1):
        if i < echo_length:
            new_list_unpacked_with_echo.append(sound_list_unpacked_to_echo[i])
        else:
            new_list_unpacked_with_echo.append(sound_list_unpacked_to_echo[i] + sound_list_unpacked_to_echo[i-echo_length] * 0.6)
        if new_list_unpacked_with_echo[i] > BIT_DEPTH:
            new_list_unpacked_with_echo[i] = BIT_DEPTH
        packed_value = struct.pack('<h', new_list_unpacked_with_echo[i])
        values.append(packed_value)
    print values
    noise_out.write_file(values)
    winsound.PlaySound('noise_with_class.wav', winsound.SND_FILENAME)


def mmmMMM():
    """doc string"""
    list1 = []
    for i in xrange(0, SAMPLE_LENGTH):
        base_sound_wave_value = math.sin(2.0 * math.pi * FREQUENCY * (i / SAMPLE_RATE))

        # takes base value and brings up to correct BIT_DEPTH * volume
        # volume = i / SAMPLE_LENGTH increases volume over time. #leetfx
        value = base_sound_wave_value * BIT_DEPTH * i / SAMPLE_LENGTH
        list1.append(value)
        unpacked_values_list_for_echo.append(value)

        packed_value = struct.pack('<h', value)
        values.append(packed_value)
        print packed_value
    return list1

    return unpacked_values_list_for_echo


def noise():
    """doc string"""
    list1 = []
    for i in xrange(0,SAMPLE_LENGTH):
        value_1 = math.sin(math.pi * FREQUENCY * (i / float(44100))) + math.sin(
            math.pi / float(1.01) * FREQUENCY * (i / float(44100)))
        value = (value_1 * (volume * BIT_DEPTH))
        list1.append(value)
        value = (value_1 * (volume * 32000))
        packed_value = struct.pack('<h', value)
        values.append(packed_value)
    return list1


def echo_two():
    echolist = noise()
    counter = 0
    for i in echolist:
        counter +=1
        if i <1000:
            value = i
        else:
            value = i + (echolist[counter-1000]*0.8)
        if value > 32000:
            value = 32000
        packed_value = struct.pack('<h', value)
        values.append(packed_value)


controls = {'m': (mmmMMM, "mmmMMM"),
            'n': (noise, "noise"),
            'p': (echo, "mmmMMM")}
for letters in controls:
    print letters + " makes a sound like " + controls[letters][1]


'create instance of sound'
load_noise = LoadSound("gunshot2.wav")
create_noise = CreateSound('noise_with_class.wav')




while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        keys = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            key_pressed = pygame.key.name(event.key)
            if key_pressed in controls:
                command = controls[key_pressed][0]
                command()

                # sets parameters and writes newly made value_string as sound wave
                noise_out.set_parameters(2, 2, 44100, 132300, 'NONE', 'not compressed')
                noise_out.write_file(values)

                print 'now play'
                del noise_out
                winsound.PlaySound('noise_with_class.wav', winsound.SND_FILENAME)
                # or with pygame
                # can't get this to work?
#                mmm_sound = pygame.mixer.Sound('noise_with_class.wav')
#                mmm_sound.play()
                noise_out = Sound()
                noise_out.set_parameters(2, 2, 44100, 132300, 'NONE', 'not compressed')