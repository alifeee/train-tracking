# Train tracking

Using <https://www.opentraintimes.com/maps/signalling/spc5> to get train headcodes.

Using <https://live.rail-record.co.uk/headcode/> to get trains from those headcodes.

## Requirements

- Python 3

## Setup

```bash
python -m venv env
pip install -r requirements.txt
```

## Run

### Find train

`not implemented`

### Find headcode

```bash
> python headcode.py <headcode>

Found 4 results

Result 1: https://live.rail-record.co.uk/train/?c=W33810&d=2024-03-12
Departure time: d. 1148
From: Manchester Piccadilly
To: Sheffield
Operator: Northern
2S80 d. 1148Manchester Piccadilly Sheffield https://live.rail-record.co.uk/train/?c=W33810&d=2024-03-12

...
```
