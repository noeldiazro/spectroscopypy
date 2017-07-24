function cumplot(filename, nsamples)

fid = fopen(filename,'r');
hold on
xlabel('Time (s)')
ylabel('Voltage (V)')
grid on
for i=1:nsamples
    A = fread(fid,[8000,2],'double');
    
    %figure(1);
    %hold on
    plot(A(:,1),A(:,2));
    %hold off

    %figure(2);
    %hold on
    %plot(A(:,3),A(:,4));
    %hold off

    %pause
end
hold off

fclose(fid);