function paused_plot(filename, nsamples)

fid = fopen(filename,'r');

for i=1:nsamples
    A = fread(fid,[8000,2],'double');
    t = A(:,1);
    v = A(:,2);
    plot(t, v);
    xlabel('Time (s)');
    ylabel('Voltage (V)');
    grid on;
    axis([-0.000003, 0.000013, -1, 9]);
    clc;
    disp('Press a key to show next pulse.');
    pause
end

fclose(fid);