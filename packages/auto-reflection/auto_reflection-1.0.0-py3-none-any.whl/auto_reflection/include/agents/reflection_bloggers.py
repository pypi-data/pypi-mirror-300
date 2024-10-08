from ..common import *
from ..config import init_config


apc = init_config.apc

if apc.llm_api=='openai':   
    from ..openai_AssistantAgent import AssistantAgent  
else:
    raise Exception(f"LLM API not supported: {apc.llm_api}")

plog=apc.plog
class Writer():
    def __init__(self, verbose=apc.verbose):
        self.data, self.vars =data, vars = apc.data, apc.vars
        self.verbose=verbose
        #self.task = task    
        self.agent_response = None
        self.agent_name=agent_name="Writer"
        self.writer_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
        self.latest=[]
        if self.verbose:
            promp(self.writer_sysmsg, f"{self.agent_name}  system prompt")
        apc.ppl_log['writer_sysmsg']=self.writer_sysmsg
        llm_config = data['llm_config']
        self.agent = AssistantAgent(
            name=agent_name,
            system_message=self.writer_sysmsg,
            llm_config=llm_config
        )  
        #self.writer.chat_history.append({"role": "user", "content": task})
        self.history=[]
    def add_history(self, messages):
        self.agent.chat_history += messages        
    def generate_reply(self, task_name, mock=None, response_format=None):
        mocked_response=None
        mocked=''
        if mock:

            magent=mock["agent_name"]
            
            assert magent==self.agent_name, f"Agent name mismatch: {magent}!={self.agent_name}"
            
            
            
            mocked_response=mock['msg']
            mocked='(mocked)'
            

        task = self.data['agents']['Writer']['tasks'][task_name].format(**self.vars)
        
        agent_response= self.agent.generate_reply(task, mocked_response=mocked_response,response_format=response_format)    
        self.history.append([task_name, task,agent_response])
        if self.verbose:  
            resp(agent_response, f'{self.agent_name} Response #{len(self.history)} {mocked}:')
        self.agent_response = agent_response
        plog(self.agent_name, agent_response)
        return agent_response
    def get_latest_history(self):
        task_name, task,agent_response = self.history[-1]
        user_history={"role": "user", "content": f'{task_name}:{task}'}
        agent_history={"role": "assistant", "content": f"{self.agent_name}'s respose to {task_name}: {agent_response}"}   
        return [user_history, agent_history]
    
    
class Critic():
    def __init__(self,  verbose=apc.verbose):
        data, vars = apc.data, apc.vars
        self.verbose=verbose
        self.history=[]
        #self.receiever = receiever
        #self.recepient = recepient
        self.agent_name=agent_name="Critic"
        self.reflection_prompt = data['agents'][agent_name]['reflection_prompt']
        self.critic_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
        apc.ppl_log['critic_sysmsg']=self.critic_sysmsg
        if self.verbose:
            promp(self.critic_sysmsg, f"{self.agent_name}  system prompt")
        llm_config = data['llm_config']
        self.agent = AssistantAgent(
            name=agent_name,
            system_message=self.critic_sysmsg,
            llm_config=llm_config
        )  
    def add_history(self, messages):
        self.agent.chat_history += messages


    def reflect_with_llm(self, mock=None, response_format=None):
        mocked_response=None
        mocked=''
        if mock:

            magent=mock["agent_name"]
            
            assert magent==self.agent_name, f"Agent name mismatch: {magent}!={self.agent_name}"
            
            
            
            mocked_response=mock['msg']
            mocked='(mocked)'        


        agent_response= self.agent.reflect_with_llm(self.reflection_prompt, mocked_response=mocked_response, response_format=response_format)    
        if self.verbose:  
            resp(agent_response, f"{self.agent_name}'s Response {mocked}:")
        self.history.append(['reflection_prompt', self.reflection_prompt,agent_response])
        self.agent_response = agent_response
        plog(self.agent_name, agent_response)
        
        return agent_response  
    def get_latest_history(self):
        task_name, task,agent_response = self.history[-1]
        user_history={"role": "user", "content": f'{task_name}:{task}'}
        agent_history={"role": "assistant", "content": f"{self.agent_name}'s respose to {task_name}: {agent_response}"}   
        return [user_history, agent_history]            
    
class Reviewer():
    def __init__(self,agent_name,   verbose=apc.verbose):
        data, vars = apc.data, apc.vars
        self.verbose=verbose
        self.history=[]
        #self.recepient = recepient
        self.agent_name=agent_name
        self.reflection_prompt = data['agents'][agent_name]['reflection_prompt']
        self.agent_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
        apc.ppl_log[f'{agent_name}_sysmsg']=self.agent_sysmsg
        if self.verbose:
            promp(self.agent_sysmsg, f"{self.agent_name}  system prompt")

        llm_config = data['llm_config']
        self.agent = AssistantAgent(
            name=agent_name,
            system_message=self.agent_sysmsg,
            llm_config=llm_config
        )  
    def add_history(self, messages):
        self.agent.chat_history += messages


    def reflect_with_llm(self, mock=None, response_format=None):
        mocked_response=None
        mocked=''
        if mock:

            magent=mock["agent_name"]
            
            assert magent==self.agent_name, f"Agent name mismatch: {magent}!={self.agent_name}"
            
            
            
            mocked_response=mock['msg']
            mocked='(mocked)'          

        print(self.agent_name, len(self.agent.chat_history))
        agent_response= self.agent.reflect_with_llm(self.reflection_prompt, mocked_response=mocked_response, response_format=response_format)    
        if self.verbose:  
            resp(agent_response, f"{self.agent_name}'s Response {mocked}:")
        self.history.append(['reflection_prompt', self.reflection_prompt,agent_response])
        self.agent_response = agent_response
        plog(self.agent_name, agent_response)
        return agent_response 
    def get_latest_history(self):
        task_name, task,agent_response = self.history[-1]
        user_history={"role": "user", "content": f'{task_name}:{task}'}
        agent_history={"role": "assistant", "content": f"{self.agent_name}'s respose to {task_name}: {agent_response}"}   
        return [user_history, agent_history]    
    
class Summarizer():
    def __init__(self, agent_name,  verbose=apc.verbose):
        data, vars = apc.data, apc.vars
        self.verbose=verbose
        self.history=[]
        #self.recepient = recepient
        self.agent_name=agent_name
        self.summary_prompt = data['agents'][agent_name]['summary_prompt']
        self.agent_sysmsg=data['agents'][agent_name]['system_message'].format(**vars)
        apc.ppl_log[f'{agent_name}_sysmsg']=self.agent_sysmsg
        if self.verbose:
            promp(self.agent_sysmsg, f"{self.agent_name}  system prompt")
        llm_config = data['llm_config']
        self.agent = AssistantAgent(
            name=agent_name,
            system_message=self.agent_sysmsg,
            llm_config=llm_config
        )  
    def add_history(self, messages):
        self.agent.chat_history += messages


    def summarize(self, mock=None, response_format=None):
        mocked_response=None
        mocked=''
        if mock:

            magent=mock["agent_name"]
            
            assert magent==self.agent_name, f"Agent name mismatch: {magent}!={self.agent_name}"
            
            
            
            mocked_response=mock['msg']
            mocked='(mocked)'   

        agent_response= self.agent.summarize(self.summary_prompt, mocked_response=mocked_response, response_format=response_format)    
        if self.verbose:  
            resp(agent_response, f"{self.agent_name}'s Response {mocked}:")
        self.history.append(['summary_prompt', self.summary_prompt,agent_response])
        self.agent_response = agent_response
        plog(self.agent_name, agent_response)
        return agent_response 
    def get_latest_history(self):
        task_name, task,agent_response = self.history[-1]
        user_history={"role": "user", "content": f'{task_name}:{task}'}
        agent_history={"role": "assistant", "content": f"{self.agent_name}'s respose to {task_name}: {agent_response}"}   
        return [user_history, agent_history]       