weights = [158.0, 164.2, 160.3, 159.9, 162.1, 164.6, 
            169.6, 167.4, 166.4, 171.0, 171.2, 172.6]

weight = 160.0   # initial guess
gain_rate = -1.0 # initial guess

time_step = 1.0
weight_scale = 4.0 / 10
gain_scale = 1.0 / 3

estimates = [weight]
predictions = []

for z in weights:
    prev_estimate = weight
    
    # Prediction step
    weight = weight + gain_rate * time_step
    predictions.append(weight)
    
    # Update step
    residual = z - weight
    gain_rate = gain_rate + gain_scale * (residual / time_step)
    weight = weight + weight_scale * residual
    
    estimates.append(weight)
    
    # Print in required format
    print(f"previous estimate: {prev_estimate:.2f}, "
          f"prediction: {predictions[-1]:.2f}, "
          f"estimate: {weight:.2f}")


