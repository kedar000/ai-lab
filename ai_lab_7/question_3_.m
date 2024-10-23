function [value] = bandit_nonstat(action)
    persistent q_true;
    persistent q_est;
    persistent action_count;
    persistent epsilon;
    
    k = 10;
    
    if isempty(q_true)
        q_true = zeros(1, k);
        q_est = zeros(1, k);
        action_count = zeros(1, k);
        epsilon = 0.1;
    end
    
    q_true = q_true + normrnd(0, 0.01, 1, k);
    
    if nargin == 0
        if rand < epsilon
            action = randi(k);
        else
            [~, action] = max(q_est);
        end
    end
    
    reward = normrnd(q_true(action), 1);
    
    action_count(action) = action_count(action) + 1;
    
    q_est(action) = q_est(action) + (reward - q_est(action)) / action_count(action);
    
    value = reward;
end