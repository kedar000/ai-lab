num_arms = 10;             
num_steps = 10000;        
epsilon = 0.1;            
q_est = zeros(1, num_arms); 
n_selected = zeros(1, num_arms); 
total_rewards = zeros(1, num_steps); 
m = ones(1, num_arms);   

for step = 1:num_steps
    if rand > epsilon
        [~, action] = max(q_est); 
    else
        action = randi(num_arms); 
    end
    
    [reward, m] = nonStatReward(action, m); 
    
    n_selected(action) = n_selected(action) + 1;
    
    q_est(action) = q_est(action) + (reward - q_est(action)) / n_selected(action);
    
    total_rewards(step) = reward; 
end

figure;
average_rewards = cumsum(total_rewards) ./ (1:num_steps); 
plot(1:num_steps, average_rewards, 'r');
xlabel('Time Steps');
ylabel('Average Reward');
title('Epsilon-Greedy Algorithm: Average Reward over Time');
grid on;