#! /usr/bin/env python

import rospy
import numpy
import random
import time

import qlearn
import lidar_env

if __name__ == '__main__':
    rospy.init_node('rl_agent_tb')
    env = lidar_env.Turtlebot_Lidar_Env()
    
    qlearn = qlearn.QLearn2(actions=range(env.nA), states=env.state_space,
                    alpha=0.2, gamma=0.8, epsilon=0.9)
    
    initial_epsilon = qlearn.epsilon

    epsilon_discount = 0.9986

    start_time = time.time()
    total_episodes = 10000
    highest_reward = 0
    
    last_time_steps = numpy.ndarray(0)

    save_freq = 100

    #qlearn.loadModel("simpleQLearning.npy")
    
    for x in range(total_episodes):
        done = False
        
        cumulated_reward = 0 #Should going forward give more reward then L/R ? 
        
        state = env.reset_env()
        
        if qlearn.epsilon > 0.05:
            qlearn.epsilon *= epsilon_discount

        
        for i in range(1500):
            # Pick an action based on the current state
            action = qlearn.chooseAction(state)
            # Execute the action and get feedback
            nextState, reward, done, info = env.step(action)
            cumulated_reward += reward
            
            if highest_reward < cumulated_reward:
                highest_reward = cumulated_reward


            
            qlearn.learn_Q(state, action, reward, nextState)
            
            #print "range" , i, "Done ", done
            if not(done):
                state = nextState
            else:
                last_time_steps = numpy.append(last_time_steps, [int(i + 1)])
                break

        if x % save_freq == 0:
            qlearn.saveModel("simpleQLearning")

        m, s = divmod(int(time.time() - start_time), 60)
        h, m = divmod(m, 60)
        print ("EP: "+str(x+1)+" - [alpha: "+str(round(qlearn.alpha,2))+" - gamma: "+str(round(qlearn.gamma,2))+" - epsilon: "+str(round(qlearn.epsilon,2))+"] - Reward: "+str(cumulated_reward)+"     Time: %d:%02d:%02d" % (h, m, s))