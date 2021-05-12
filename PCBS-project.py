import numpy as np
import expyriment
import matplotlib.pyplot as plt


time_between_beeps=75
time_between_flashes=68
pre_stimulus_time=750
stimuli=2*[(beeps,flashes) for flashes in range(1,5) for beeps in range(flashes+1)]+5*[(beeps,1) for beeps in range(5)]
trials=stimuli
np.random.shuffle(trials)
data_obtained=[]

instructions = "Welcome to this flash and beeps experiment! \n \
                \nRead the following instruction carefully:\n \
                \nKeep your eyes fixed on the cross in the middle of the screen.\n \
                \nIn each trial, you will see between one and four flashes and you may hear beeps.\n \
                \nAt the end of each trial, report the NUMBER OF FLASHES seen by pressing 1,2,3 or 4 on your keyboard\n \
                \nEach trial lasts for less than two seconds.\n \
                \nYou will do the task 62 times and you can take a break between each task.\n\
                \nPress the SPACEBAR to start the experiment."
                
                
experiment = expyriment.design.Experiment(name="Auditory over Visual?")
expyriment.control.initialize(experiment)

#Stimuli
fixation_cross = expyriment.stimuli.FixCross()
visual_stimulus =expyriment.stimuli.Circle(60, position=(0,-200),colour=(255,255,255))
beep_stimulus=expyriment.stimuli.Tone(frequency=880, duration=7)
visual_stimulus.preload()
beep_stimulus.preload()
fixation_cross.preload()

expyriment.control.start(skip_ready_screen=True)
expyriment.stimuli.TextScreen("INSTRUCTIONS", instructions).present()
experiment.keyboard.wait(expyriment.misc.constants.K_SPACE)
for trial in trials:
    number_of_beeps,number_of_flashes=trial
    data_obtained.append([number_of_beeps,number_of_flashes,0])
    fixation_cross.present()
    experiment.clock.wait(pre_stimulus_time)
    experiment.clock.reset_stopwatch()
    while True :
        if (experiment.clock.stopwatch_time)%time_between_beeps==0 and number_of_beeps>0:
            number_of_beeps-=1
            beep_stimulus.present()
            experiment.clock.wait(2)
        if (experiment.clock.stopwatch_time+52)%time_between_beeps==0 and number_of_flashes>0:
            fixation_cross.present()
            visual_stimulus.present(clear=False)
            number_of_flashes-=1    
            experiment.clock.wait(time_between_flashes//2)
            fixation_cross.present()
        if number_of_beeps==0 and number_of_flashes==0:
            break
    number_of_flashes_seen,reaction_time=experiment.keyboard.wait([expyriment.misc.constants.K_KP1,expyriment.misc.constants.K_KP2,
                              expyriment.misc.constants.K_KP3,expyriment.misc.constants.K_KP4])
    data_obtained[-1][2]=number_of_flashes_seen%256
print(data_obtained)
expyriment.control.end()

#Data treatment
#Influence of the beeps with one flash
one_flash=[]
for result in data_obtained : 
    number_of_flashes=result[1]
    if number_of_flashes==1: one_flash.append(result)
one_flash_beeps=[[] for i in range(5)] 
for result in one_flash : 
    number_of_beeps,number_of_flashes,number_of_flashes_seen=result
    one_flash_beeps[number_of_beeps].append(number_of_flashes_seen)
mean_flash_seen_per_beeps=[]
for n_beeps in range(5):
    mean_flash_seen_per_beeps.append(np.mean(one_flash_beeps[n_beeps]))

plt.figure()
plt.plot([0,1,2,3,4], mean_flash_seen_per_beeps,color='black')
plt.xlabel("#Beeps")
plt.xticks([0,1,2,3,4])
plt.yticks([1,2,3])
plt.ylabel("#Perceived flashes")
plt.title("Influence of the beeps with #flashes=1")

#No beeps results // Control trial
no_beep=[]
for result in data_obtained : 
    number_of_beeps=result[0]
    if number_of_beeps==0 : no_beep.append(result)
no_beep_flashes=[[] for i in range(4)]
for result in no_beep :
    number_of_beeps,number_of_flashes,number_of_flashes_seen=result
    no_beep_flashes[number_of_flashes-1].append(number_of_flashes_seen)
mean_perceived_flash_no_beep=[np.mean(no_beep_flashes[n_flashes]) for n_flashes in range(4)]


plt.figure()
plt.plot([1,2,3,4], mean_perceived_flash_no_beep,color='black',linestyle='dashed')
plt.scatter([1,2,3,4], mean_perceived_flash_no_beep,color='black')
plt.xlabel("#Flashes")
plt.xticks([1,2,3,4])
plt.yticks([1,2,3,4])
plt.ylabel("#Perceived_flashes")
plt.title("Control experiment (with no beep)")
