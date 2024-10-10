# A Python Wrapper for the Stormwater Management Model (SWMM5)

```python

import swmm

# Create a SWMM model object
error_code = swmm.swmm_open("path/to/swmm5.inp", "path/to/swmm5.rpt", "path/to/swmm5.out")
error_code = swmm.swmm_start(True)

# Run the SWMM model
current_time = swmm.getValue(swmm.swmm_CURRENTDATE, 0)
end_time = swmm.getValue(swmm.swmm_ENDDATE, 0)

# Run the model until the end time
while current_time < end_time:
    elapsed_time = swmm.swmm_step()
    current_time = swmm.getValue(swmm.swmm_CURRENTDATE, 0)
    
# Close the SWMM model
error_code = swmm.swmm_end()
error_code = swmm.swmm_report()
error_code = swmm.swmm_close()


```
    

