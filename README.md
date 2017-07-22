# RailIN

This API scrapes data of Indian Railways and parses into JSON for use in personal applications.

<b>Strictly Not intended for commercial use.</b>

1. Get Route
2. Get Availability
3. Get Fare
4. Get Train Status
5. Get TrainInfo
6. Get PNR Status

Example Usage:

`from RailIN import RailIN

ri = RailIN()
ri.getPNR('1234567890')

`
<i> Output is in JSON format load using json package.

All Responses are subjected to Server's state.

I strictly do not claim any right over the data. And by no means promote usage of it for commercial applications.

Data and it's rights reserved to respective owners.
