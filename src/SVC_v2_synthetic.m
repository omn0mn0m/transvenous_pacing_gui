function [x,ecg_svc]= SVC_v2_synthetic(rate)
% superior vena cava 
x=0.01:0.01:2;
% default=input('Press 1 if u want default ecg signal else press 2:\n'); 
% if(default==1)
      %li=30/72;  
     %rate=input('\n\nenter the heart beat rate :');
     li=30/rate;
    
      a_pwav=-0.1;
      d_pwav=0.12;
      t_pwav=0.17;  
     
      a_qwav=-.0025;
      d_qwav=0.066;
      t_qwav=0.166;
      
      a_qrswav=-0.1;
      d_qrswav=0.07;
      
      a_swav=-0.0025;
      d_swav=0.066;
      t_swav=0.09;
      
      a_twav=0.05;
      d_twav=0.3;
      t_twav=0.2;
      
%pwav output
 pwav=p_wav(x,a_pwav,d_pwav,t_pwav,li);

 
 %qwav output
 qwav=q_wav(x,a_qwav,d_qwav,t_qwav,li);

    
 %qrswav output
 qrswav=qrs_wav(x,a_qrswav,d_qrswav,li);

 %swav output
 swav=s_wav(x,a_swav,d_swav,t_swav,li);

 
 %twav output
 twav=t_wav(x,a_twav,d_twav,t_twav,li);

 %ecg output
 
 
 ecg_svc=pwav+qrswav+twav+swav+qwav;

 %figure(1)
 %plot(x,ecg_svc);
