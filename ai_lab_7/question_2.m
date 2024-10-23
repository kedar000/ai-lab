Q = zeros(1,2);  
N = zeros(1,2);  
e = 0.1;  
num_iterations = 10000;  

avg = zeros(1, num_iterations);

for i = 1:num_iterations
    if(rand > e)
        [m, A] = max(Q);  
    else
        temp = randperm(2);  
        A = temp(1);
    end
    
    R = binaryBanditB(A);  
    
    N(A) = N(A) + 1;
    
    Q(A) = Q(A) + (R - Q(A)) / N(A);
    
    if i == 1
        avg(i) = R;  
    else
        avg(i) = ((i-1) * avg(i-1) + R) / i;  
    end
end

disp('Final Q-values:');  
disp(Q);
disp('Number of times each action was selected:');
disp(N);
disp('Final average reward:');
disp(avg(end));

figure;
plot(1:num_iterations, avg, 'r');
xlabel('Iterations');
ylabel('Average Reward');
title('Epsilon-Greedy Algorithm: Average Reward over Time');
ylim([0 1]);
grid on;