class env():
    def __init__(self):  # vehicle agent is an instant from Auto-vehicle class
        self.ActionsList = ["ChangeLR", "ChangeLF", "fast", "slow", "stop", "DoNothing"]
        self.ActionsDict = {"ChangeLR": 0, "ChangeLF": 1, "fast": 2, "slow": 3, "stop": 4, "DoNothing": 5}
        # self.agent = vehicleAgent

    def Reward(self, agent):
        try:
            agent.car.UpdateStatus()
            agent.car.reward = 0
            if agent.car.isStop() == False:
                agent.car.reward += 1

            agent.car.reward -= agent.car.wait_time()

            agent.car.reward += (agent.car.spd / agent.car.maxspeed) * 10

            nonlane_vehicle_num = traci.edge.getLastStepVehicleNumber(
                agent.car.edge) - traci.lane.getLastStepVehicleNumber(agent.car.lane)
            if traci.lane.getLastStepVehicleNumber(agent.car.lane) == max(
                    traci.lane.getLastStepVehicleNumber(agent.car.lane), nonlane_vehicle_num):
                agent.car.reward += traci.lane.getLastStepVehicleNumber(agent.car.lane) - nonlane_vehicle_num
            else:
                agent.car.reward += traci.lane.getLastStepVehicleNumber(agent.car.lane) - nonlane_vehicle_num
        except:
            pass
        # print("Reward :", self.agent.reward)

    def Current_state(self, agent):
        '''
        Traffic state on the lane
        # of cares in the lane
        my speed
        avg speed of the cares in my lane
        '''
        agent.car.UpdateStatus()
        try:
            state = (agent.car.next_TL(), agent.car.spd, traci.lane.getLastStepMeanSpeed(agent.car.lane))
            print(state)
        except:
            pass

    def getFeasibleActions(self, agent):

        left = 1
        right = -1
        changeLeftPossible = traci.vehicle.couldChangeLane(agent.ID, left, state=None)
        changeRightPossible = traci.vehicle.couldChangeLane(agent.ID, right, state=None)
        _, leaderDist = trace.getLeader(agent.ID)
        accelerate_possible = min(agent.maxspeed, agent.spd + agent.maxacc / 2) <= leaderDist
        proposedActions = actionList.copy()
        if changeLeftPossible == False:
            proposedActions.remove("changeLF")
        if changeRightPossible == False:
            proposedActions.remove("changeLR")
        if accelerate_possible == False:
            proposedActions.remove("fast")
        return proposedActions
