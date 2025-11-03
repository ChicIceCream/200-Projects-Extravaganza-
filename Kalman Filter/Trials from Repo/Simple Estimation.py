weights = [158.0, 164.2, 160.3, 159.9, 162.1, 164.6, 
            169.6, 167.4, 166.4, 171.0, 171.2, 172.6]

time_step = 1   # days
scale_factor = 0.4  # filter gain

def prediction_using_gain(estimated_weight, gain_rate, do_print=True):
    for measurement in weights:
        prev_estimate = estimated_weight
        
        # Predict
        predicted_weight = prev_estimate + gain_rate * time_step
        
        # Update
        estimated_weight = predicted_weight + scale_factor * (measurement - predicted_weight)
        
        if do_print:
            print(f"previous estimate: {prev_estimate:.2f}, "
                    f"prediction: {predicted_weight:.2f}, "
                    f"estimate: {estimated_weight:.2f}")

initial_estimate = 160
prediction_using_gain(initial_estimate, gain_rate=1, do_print=True)