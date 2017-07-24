%% Define Red Pitaya as TCP/IP object
clc
clear all
close all
IP= '192.168.1.8';           % Input IP of your Red Pitaya...
port = 5000;                                  
tcpipObj=tcpip(IP, port);       

tcpipObj.InputBufferSize = 8000 * 64;
tcpipObj.OutputBufferSize = 8000 * 64;
flushinput(tcpipObj);
flushoutput(tcpipObj);

%% Open connection with your Red Pitaya and close previous
instrument = instrfind;
fclose(instrument);

fopen(tcpipObj);
tcpipObj.Terminator = 'CR/LF';

%% Calculate arbitrary waveform with 16384 samples
% Values of arbitrary waveform must be in range from -1 to 1.
fid = fopen('bi_207_amp.dat','r');
A = fread(fid,[8000,2],'double');
t = A(:,1)'*10^6;
x = (A(:,2))';
plot(t,x);
grid on
%waveform_ch_1_0 = num2str(x, '%1.5f,');
%waveform_ch_1 = waveform_ch_1_0(1, 1:length(waveform_ch_1_0)-3);
fclose(fid);
%N = 16383;
%t = 0:(2*pi)/N:2:pi;
%x = sin(t)+1/3*sin(3*t);
waveform_ch_1_0 = num2str(x, '%1.5f,');
waveform_ch_1 = waveform_ch_1_0(1,1:length(waveform_ch_1_0)-3);

%% The example generate sine bursts every 0.5 seconds indefinety
fprintf(tcpipObj,'GEN:RST');
pause(2)

fprintf(tcpipObj,'SOUR1:FUNC ARBITRARY');
fprintf(tcpipObj,['SOUR1:TRAC:DATA:DATA ' waveform_ch_1]);
%fprintf(tcpipObj,['SOUR1:TRAC:DATA:DATA ' waveform_ch_1]);
fprintf(tcpipObj,'SOUR1:FREQ:FIX 32000');     % Set frequency of output signal
fprintf(tcpipObj,'SOUR1:VOLT 1');          % Set amplitude of output signal

fprintf(tcpipObj,'SOUR1:BURS:STAT ON');    % Set burst mode to ON
fprintf(tcpipObj,'SOUR1:BURS:NCYC 1');       % Set 1 pulses of sine wave
%fprintf(tcpipObj,'SOUR1:BURS:NOR 4');    % Infinity number of sine wave pulses
%fprintf(tcpipObj,'SOUR1:BURS:INT:PER 2500'); % Set time of burst period in microseconds = 5 * 1/Frequency * 1000000
pause(2)
fprintf(tcpipObj,'OUTPUT1:STATE ON');         % Set output to ON


%% Close connection with Red Pitaya

fclose(tcpipObj);