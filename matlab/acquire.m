function acquire(filename, nsamples)
% Acquire spectroscopy pulses
% filename: output file to store acquired pulses
% nsamples: number of pulses to acquire

% ---------------------------------
% HP54505B instrument configuration
% ---------------------------------

% Create and configure instrument control object
osc = visa('agilent','GPIB0::7::INSTR'); % Instrument on GPIB address 7
osc.EOIMode = 'on';
osc.EOSMode = 'none';
osc.Timeout=10.0;   % Give enough time for all data to be transfered
osc.inputBufferSize=16384;
osc.ByteOrder='bigEndian';

% Connect with instrument and set default values
fopen(osc);
clrdevice(osc);
fprintf(osc,'*CLS');
fprintf(osc,'*RST');

% Set config to trigger capture when signal on channel 1 
% goes above 0.25 volts
fprintf(osc,'TRIGGER:Mode EDGE');
fprintf(osc,'TRIGGER:Source CHANNEL1');
fprintf(osc,'TRIGGER:Level 0.25 V');
fprintf(osc,'TRIGGER:SLOPE POSITIVE');

% Set signal range between 0-10 volts
fprintf(osc,'CHANNEL1:Range 12');
fprintf(osc,'CHANNEL1:Offset 5');

% Set sampling acquisition to 500 MHz and sampling duration to 16 us
% Capture starts 3 us before triggering
% ACQUIRE:Points   TIMEBASE:Range   Medida
% 8000             1 us             fs = 500 MHz durante 16 us
% 8000             2 us             fs = 250 MHz durante 32 us
fprintf(osc,'TIMEBASE:Sample REALTIME');
fprintf(osc,'TIMEBASE:Delay -3 us');
fprintf(osc,'TIMEBASE:Reference LEFT');
fprintf(osc,'TIMEBASE:Range 1 us');
fprintf(osc,'ACQUIRE:Points 8000');

% Set resolution to 15 bits
% WAVEFORM:Format   Resolución
% BYTE              7 bits
% WORD              15 bits
fprintf(osc,'WAVEFORM:Format WORD');

% Measurements
fid = fopen(filename,'a');
for i=1:nsamples
    % Get the pulse that comes first
    fprintf(osc,'DIGITIZE Channel1');
    % Ask for the waveform of the pulse on channel 1
    [t1, v1] = getData(osc,'1');

    % Write waveform to the output file
    fwrite(fid, [t1 v1], 'double');
    
    % Continue
    fprintf(osc,'RUN');
end

fclose(fid);
fclose(osc);
delete(osc);
end

function [t,v] = getData(osc,channel)
    
    fprintf(osc,strcat('WAVEFORM:Source CHANNEL',channel));
    
    fprintf(osc,'WAVEFORM:Data?');
    
    s = binblockread(osc,'int16');
    
    fprintf(osc,'WAVEFORM:XINCREMENT?');
    xincrement=str2double(fscanf(osc));
    fprintf(osc,'WAVEFORM:XORIGIN?');
    xorigin=str2double(fscanf(osc));
    fprintf(osc,'WAVEFORM:XREFERENCE?');
    xreference=str2double(fscanf(osc));
    fprintf(osc,'WAVEFORM:YINCREMENT?');
    yincrement=str2double(fscanf(osc));
    fprintf(osc,'WAVEFORM:YORIGIN?');
    yorigin=str2double(fscanf(osc));
    fprintf(osc,'WAVEFORM:YREFERENCE?');
    yreference=str2double(fscanf(osc));   
    
    v=(s-yreference)*yincrement+yorigin;
    t=((1:length(v))'-xreference)*xincrement+xorigin;
end
