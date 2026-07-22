"""
KPI Library Demo Dashboard
Streamlit in Snowflake — one page per Area, each showing live DEMEAU examples
of every KPI/chart in the Ditteau KPI Library.

Target database: DEMEAU_DD_DEV, schema: DISTRIBUTE
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAAb8AAAHRCAIAAAB1jyAPAAAKKGlDQ1BpY2MAAEiJlZYHUBTZFoZP9+TEADNECUPOCEMaQHJOkqOojDNkGGGIImYWV3ANqEgwIgZEwVUJskZEMSACCpgXZBFRn4sBUVF5jezq7tuq9+qdrlvn69Pd/z23b1f1D0Dbw09LS0ElAVJFmeIgD2dORGQUh/QbUEAKaGAKHL4gI80pIMAXsPgz/z3e9QEynW8ZTWv98/p/DWlhbIYAAInGOFmYIUjF+ArGcwRp4kwAFI+xRk5m2jTrYswWYw1iPGea42c4YJoXzbDw6z0hQS4Y5wKQ6Xy+OB6AWoDVOdmCeEyHWo2xiUiYKML4Nsb2ggQ+9hyNjbFhauriaXbEWBe7Pw3jBIx5i/6iGf83/UXf9Pn8+G88s66vIeXq5uvLceNyeeHuAZwcYeb/+Y7+Z6SmZP051/RO0GNFocHTPWBDCVzBDXyxg4NlLnbwIBzcIQA7zwEhZGbG5n7tx2Vx2hJxYnxCJscJ28VYjpdIYGzI4ZpwTQCmv4kZ+TdKX2dA9Iy/11LOAVjNB8AZfK8J9wM0FwPIPfhe0xIDSMpjdW1Bljh7pja9vUAAKjCBDQqgAhqgC0ZYl5ZgC45Yx97gDyEQCQtAAAmQCmKs63xYBYVQDJtgG1TAbtgHh+AoHIcmOA0X4DJchy7ohfswAMPwHMbgHUwiCEJCGAgLUUBUES3EAOEiPMQecUN8kSAkEolB4hERkoXkI2uQYqQEqUD2IjXIz8gp5AJyFelG7iKDyCjyGvmI4lA6ykaVUW10NspDnVAfNASdj8aj6WgeWoBuQMvQKvQI2oheQK+jvegA+hwdxwGOhpPFqeGMcDycC84fF4WLw4lxy3FFuFJcFa4O14Jrx93CDeBe4D7giXgWnoM3wtviPfGheAE+Hb8cvx5fgT+Eb8S34W/hB/Fj+C8EBkGJYECwIXgRIgjxhBxCIaGUcIDQQLhE6CUME94RiURZog7RiuhJjCQmEZcS1xN3EuuJ54ndxCHiOIlEUiAZkOxI/iQ+KZNUSConHSGdI/WQhknvyTSyKplLdidHkUXk1eRS8mHyWXIPeYQ8SZGkaFFsKP4UIWUJZSOlmtJCuUkZpkxSpag6VDtqCDWJuopaRq2jXqI+oL6h0WjqNGtaIC2RtpJWRjtGu0IbpH2gS9P16S70aHoWfQP9IP08/S79DYPB0GY4MqIYmYwNjBrGRcYjxnsJloSxhJeEUGKFRKVEo0SPxEsmhanFdGIuYOYxS5knmDeZLyQpktqSLpJ8yeWSlZKnJPslx6VYUqZS/lKpUuulDktdlXoqTZLWlnaTFkoXSO+Tvig9xMKxNFguLAFrDauadYk1zCayddhe7CR2Mfsou5M9JiMtYy4TJpMrUylzRmZAFierLeslmyK7Ufa4bJ/sRzllOSe5WLl1cnVyPXIT8rPkHeVj5Yvk6+V75T8qcBTcFJIVNis0KTxUxCvqKwYq5ijuUryk+GIWe5btLMGsolnHZ91TQpX0lYKUlirtU+pQGldWUfZQTlMuV76o/EJFVsVRJUllq8pZlVFVlqq9aqLqVtVzqs84MhwnTgqnjNPGGVNTUvNUy1Lbq9apNqmuox6qvlq9Xv2hBlWDpxGnsVWjVWNMU1XTTzNfs1bznhZFi6eVoLVdq11rQltHO1x7rXaT9lMdeR0vnTydWp0HugxdB9103Srd23pEPZ5est5OvS59VN9CP0G/Uv+mAWpgaZBosNOg25BgaG0oMqwy7DeiGzkZZRvVGg0ayxr7Gq82bjJ+OVtzdtTszbPbZ38xsTBJMak2uW8qbeptutq0xfQ1V58r4FZyb5sxzNzNVpg1m70yNzCPNd9lfseCZeFnsdai1eKzpZWl2LLOctRK0yrGaodVP4/NC+Ct512xJlg7W6+wPm39wcbSJtPmuM3vtka2ybaHbZ/O0ZkTO6d6zpCduh3fbq/dgD3HPsZ+j/2Ag5oD36HK4bGjhqPQ8YDjiJOeU5LTEaeXzibOYucG5wkXG5dlLuddca4erkWunW7SbqFuFW6P3NXd491r3cc8LDyWepz3JHj6eG727PdS9hJ41XiNeVt5L/Nu86H7BPtU+Dz21fcV+7b4oX7eflv8HszVmiua2+QP/l7+W/wfBugEpAf8EkgMDAisDHwSZBqUH9QezApeGHw4+F2Ic8jGkPuhuqFZoa1hzLDosJqwiXDX8JLwgYjZEcsirkcqRiZGNkeRosKiDkSNz3Obt23ecLRFdGF033yd+bnzry5QXJCy4MxC5kL+whMxhJjwmMMxn/j+/Cr++CKvRTsWjQlcBNsFz4WOwq3C0Vi72JLYkTi7uJK4p/F28VviRxMcEkoTXiS6JFYkvkryTNqdNJHsn3wweSolPKU+lZwak3pKJC1KFrUtVlmcu7g7zSCtMG0g3SZ9W/qY2Ed8IAPJmJ/RnMnGfr4dWbpZP2QNZttnV2a/zwnLOZErlSvK7Viiv2TdkpE897z9S/FLBUtb89XyV+UPLnNatnc5snzR8tYVGisKVgyv9Fh5aBV1VfKqG6tNVpesfrsmfE1LgXLByoKhHzx+qC2UKBQX9q+1Xbv7R/yPiT92rjNbV77uS5Gw6FqxSXFp8af1gvXXfjL9qeynqQ1xGzo3Wm7ctYm4SbSpb7PD5kMlUiV5JUNb/LY0buVsLdr6dtvCbVdLzUt3b6duz9o+UOZb1lyuWb6p/FNFQkVvpXNl/Q6lHet2TOwU7uzZ5birbrfy7uLdH/ck7rmz12NvY5V2Vek+4r7sfU+qw6rb9/P21xxQPFB84PNB0cGBQ0GH2mqsamoOKx3eWIvWZtWOHok+0nXU9WhznVHd3nrZ+uJjcCzr2LOfY37uO+5zvPUE70TdSa2TOxpYDUWNSOOSxrGmhKaB5sjm7lPep1pbbFsafjH+5eBptdOVZ2TObDxLPVtwdupc3rnx82nnX1yIvzDUurD1/sWIi7fbAts6L/lcunLZ/fLFdqf2c1fsrpy+anP11DXetabrltcbOyw6Gm5Y3GjotOxsvGl1s7nLuqule0732R6Hngu3XG9dvu11+3rv3N7uvtC+O/3R/QN3hHee3k25++pe9r3J+ysfEB4UPZR8WPpI6VHVr3q/1g9YDpwZdB3seBz8+P6QYOj5bxm/fRoueMJ4UjqiOlLzlPv09Kj7aNezec+Gn6c9n3xR+C+pf+14qfvy5O+Ov3eMRYwNvxK/mnq9/o3Cm4Nvzd+2jgeMP3qX+m5youi9wvtDH3gf2j+GfxyZzPlE+lT2We9zyxefLw+mUqem0vhi/lcrgMMGGhcH8PogACMSgNWFeal5M57tD2+D/Ol43vC+83vyN8byjK/7GpYA+/oBQpYC+N4AKK8A0Mb0mZjXDGBidVtAzcy+jT8iI86MO6PFdAMgaU5NjZUAUOwBPgdPTX08NzX12RDzLZUAJ11mvOJ0SB4B6JLhOnH92i6v+Yc/m/GRf1njf2b41sHf8r8BKwXEjgdZDX4AAAADc0JJVAgICNvhT+AAAABfelRYdFJhdyBwcm9maWxlIHR5cGUgQVBQMQAACJnjSk/NSy3KTFYoKMpPy8xJ5VIAA2MTLhNLE0ujRAMDAwsDCDA0MDA2BJJGQLY5VCjRAAWYGphZmhmbGZoDMYjPBQBIthTJOtRDMgAAIABJREFUeJzt3XlAVWXeB/DnXpYLlx0ETRRQcMQQVFBxS8UFTdTGlEjTHCM108zStNIhc2p6XSoty7TQLLXMzHHBzFS0ckHFXLouiQsIblcFUe7lAsL7x5lhGES8y3nOc55zvp+/GtPn/Mby23Oe5Xc0VVVVBAAAbKRlXQAAAJeQngAA9kB6AgDYA+kJAGAPpCcAgD2QngAA9kB6AgDYA+kJAGAPpCcAgD2QngAA9kB6AgDYA+kJAGAPpCcAgD2QngAA9kB6AgDYA+kJAGAPpCcAgD2QngAA9uApPS0mszG3gHUVAEALX3/AeUrPbR98tTBu3MZ3llpMZta1AICYDm/cOb9L6ic9Xio4fZ51LdbS8PJVOENm1prkOYQQjVbr7OGSkDayU8rjOr0767oAwCFn9h7Z/n8ri/682ittVFHBNcMPe1/e9QkXf7T5SE9jbsEnPV8qv2Op/hGNVuPs4YoMBeCXkJtX9+d0mf5kn0kjdHp3i8m8YnSas6vL86v/ybq6h+MgPS0m87Lk6Vez6pjPCxnaLrVfwvhk70B/6WsDADvsWfHD4eU/mq4X90obFZ3YpeYfXmNuwWeJr3Z/PaXHmCcZVmgNDtLzp4++/vWdtVWVD6mz+YC2PSalRHSMkaYqALDVjbzLOxatPvfT7+4Bnj2mPt26T+c6XxyzN+366e/p4zbPbxDSWPoirSf39Mw35Czp8bL1P98rLKDds307D0/CVBRAPnYu+fbUjweu7Dvbbly/tn/t+dBZzvdvfnT5yJ+Tty2Wpjz7yDo9LSbz3DajLYUlNv0qjVZbVVkZFBvWbdLQFp3bIkYBWNm/duvRdbuu/37Rq4l/j6lPW//n0WIyz48b03p4j7+mTaBdpN1knZ5rX/vgxMpdD31nfxCNVlNVWYUYBZDYni83nNyyt+jcNZ23e5vhvWMe7xYYGmzrIDkHj69KmT32xwXBkc1pFOk4+aanre/s9aiO0dZPdrfvHyQA1K/4RuG+lZvyDp+6cjDHq4m/3aFZ0/dvfpS3z/Dq7qViFSkumaanxWRelPDi7XPXaQzu6u0WPapXy57tm7ZugQkpgCPyDTm5R08fWLrpbv7NsD5tWg/sJuJ7nvD+Hj9pcN+JI0QZUFwyTU8r99kdoXHSVt2r9AkPavNMr/BObZq2boFzowDWMOYW5B07c/T7nee3HhV+ROerjxvXP2l6qujPMmRmbZzykTz33+WYnsbcgoVx46R/rk94UET/9i17tg9q3gRv9wDVLCaz8UJB7tHThi2/5f58gvxnb1b4uy4erh0mDqQRnYKV4+aUFpeM/3YupfHtJsf0TH92ZvV/06QnzEldvd2adIuM7Nc5tG1kYLNgTEtBbYy5BdfP5+fsPXrxl+PXj1x80E9z1rt0nDSIXnSS/0ynnt34j5ZdY+k9xQ6yS8/q++yy4hUW0CQ+slmXGIQpKJUQl/kn/szdb/j3BNNJW3Wvsp5f4tnUP2Z4T6rRKdi7estvC7+fcehL2g+yibzS02Iyf9h9/J2LN1kX8hCu3m6PxLeIGtjNt3GgT1BAk6gI1hUB2KbYeKv4+q3co6ev/Zl7af9JYXb50LisSbLoJML2Ufsxbf/Wd6Akj7OSvNJzz4offn59hfX//OTDJzwooGXjyH6dkacgQ9VZeeNCwTXDBWFq6Qgpo1NgyMz610sLpx1cLp83PxmlZ7Hx1gcdn6/ZSIlrwvy0YVSzBs2CQ9tGEkIQqSABISivncsrvWM6/dP+u1eL6lm1tI/00Sn4LPk1zyDfkZ/MlPi5DyKj9Nz4ztJDH22p3shTJCFSG/ylacO/hAqzVO8gf5w5BfvkG3IIIblHT5feKTm353fzzTvVQWnTO7hNWEUnISTfkPPFwOmT9iyWyekluaRnsfHW3FajWFchqZr/fut89Y06hOv9vZt1iSGECHNVbE8BIcSYW2C5a759/WbRZePdm4W5+w2W4pI6GzZKgGF0Cr5+8V1Lifn5le+wKqAmuaTnD299kv3JVtZVyJEwXSWEhPdo5+bl4ealbxgeQgjBpFUxhClkaYnp2tk8QsiFfcdNt4prTiQJzbmk9ZhHJyEk35Cz/Ik3UrfMlcPld1mkp4hX2hVPuLNf80eCYsPcA7wIIaGdozwD/AghDVuEuHnoCRJWBoRkJIQIC5HkP+FICLmSdbasuJRlcbaQQ3QKMualX9z3x8R/fci6EHmk5/Ln0s5tymZdhcKF9o0W/qJ6fYAQUj2TFWBf66GEPRnhr6tni4QQ4Z1a+OtbZy/ff+qu5uUc7sgnOgkhxcZbCzuPH7V2drO4KLaVsE9PTDwZquePdPWKQbWogd1q/s9ayVtNthFcM/iqCeuJNX/k2p+5N/68VP0/a71Bq5CsolMgk+mnM9vHE0J++fwH1iWoVz2zobLi0lqnAh0/JOgVFuDfguJu6b3yivzdp2z6JXJYT5Qzz6b+TTpHyio6CSGPjRmSvWxbwenzbFc/Gc89VbjVDsALtwaeDduFjU6fLcOzHxnz0q8YLrDdfNcyfDYhZMfib9gWAAB1cvVxD4wOkWd0EkLaJPW4vPfMjbzLDGtgmZ7Fxls4pQQgQ14h/g1jm41ZOUee0UkIaRIVEdorevNslm3nWabn/m8yNFrGk18AqMUrxN83vJGco1PQ++URVw7nWExmVgUwCy+LyXxg4b/4PcMBoEi8RCchpElUhHug16Z3PmdVALP0zMk6Xl5SxurpAHA/jqJTkDhrzLnth1k9nVl6Zrz+GU6KAMgHd9FJCIlKiK8oKdv3TQaTp7NJz3xDDqXvZQKAHXiMTkHCrJHZa7YzeTSb9MQJeQD54Dc6LSbziX/tMV+7bcwtkP7pDNKz2HjLsGqP9M8FgPtxHZ0rRqcVnbt6+7xx39dbpC+AQXqe2L5Po9VI/1wAqIX36Lx25MKdvFuEkKPLt0t/dIlBev764Xe1eqwBgPS4js6VqbONJ/LKbv87McuKS3OyjktchtTpmW/Ikf8nMwEUzyvEX+fnwWN0EkK+m/bBzdOXS2/crfmDB1ZskrgMqdPz4Hc/SfxEAKjFK8T/XlnFyOV/5zE6M+al5+8/ffdS7WaD57ceLTbW/kGqJE1Pi8l84utdUj4RAGpx1rtWmMvHZSwIDA1mXYvNMualH/9m9/3RSQjRaLUntu+TshhJ0zMn6zhHnyIAUB5XH72Lh278tvcVFp2EkKrKyl8//E7KeiRNz9+/3ynl4wCgJp2f3snVSZHRKbhz8aaUBz+lS0+LyXxq7V7JHgcANen89FpnJUen4MhG6dYGpUvPnKzjGif0owNgQCXRSQj5/aufaddTTbo4+/37nWgLAiA99UQnkfblXaL0xGs7ABOqik6BZC/vEqUnXtsBpKfC6CQSvrxLlGh4bQeQmDqjk0j48i5FeuK1HUBivEfnwcWb7YtOwfEffxOxngeRIj0v/XFWgqcAgID36Dz0yZYKU7kjg/zxwy9i1VMPKdLzeMavEjwFAAjn0bnzs7XZy7Y5/sWz60cuSnDnXYr0/GP1bgmeAgA6P72l0PT0yjd5jE5DZtbeBd9bikyOD6Vx0p7df9TxcepHPT2NuQWi/HYAwENZCk0j1qVFdIxhXYjNDJlZ68cuECsrqu5VnvrpgChD1YN6ev752+8aLc4qAUhhxLq0qIR41lXYTNzoFEiwU0091wxbfquqxFklALp0vnpEZy35hhzRx6yJbnpaTObcn09QfQQA6Hz1Qz+fhuis5cyv2TSGrUY3PXFWCYA2ROeDnNxM99Qn3fQ8d+AY1fEBVA7RWY+rWeepfmiTbnqe3kJ928sabgEeOj896yqAEEJ0fnq3Bp6sq1AIROdDUX39pZieFpP5+pGL9Ma3npObi5PO2bOpP+tC1M69kbel0OQdEsC6ECVAdFqD6usvxfSU1aLn6LX/SHx7jHugl0ewL+ta1Mgj2Nc9yGvIx1MGLJrAuhYlQHRa6c+fDtIbnGJ6XjubR29wO8QN7vVa9ooe04cTQvSNvFmXoxZeIf6EkB7Th792eAWPf9pliOvoXJM8R8rrM1SXPimmp2GLFG1ObKLTu3d9ZuCMU1+3HNzZ1dvN1QeLoRS5ervpfPXRT/eccerrrs8M5PHT4TLEe3RK/1zjBVrd6iimp2xPenoH+g/75+TUzXMbxoa5YxJKh0dj37A+bZ7b+F7S9FTvQKw4iwPRaYfco6cpjUwrPWmf8ndck6iIF9bNH/LxFPcgLIaKybtZQEBU8BOLJo9eltYkKoJ1Ocqh89UnfTCBx+g05hasSZ7D6twLvZdgZ0rjXjuXp9Fq5X9HMyohPuLwisMbdu6a87WLh+udPOpdrRTMt2Wj0ht3u015qv2Q3nhPF5ert1vcuP5xg3uxLsRmxtyCpf2nCs2fmBRwJYvW9jWt9Dyz67D8o1MgLIZGJ3b5dcWG7GXbqiory4pLWRfFGY9g34qSskef6PLYmCF4Txeds96l/QsDkqansi7EZkJ0VlbcYxWdhJCy4lJjbgGNln200jPvtz8ojUyJd6B/0vTUNkk9di5aU3DgTMnlItYV8UHnp3d2dw2ObzlgZiqPPSXlz62BZ+xziYhOR1w/n89NelpM5jsXb9IYmbYmURGjl6UZMrN+mp1+r+Je0ZmrrCuSNd+WjZycnQbPn8RjQ0kueDb1jxneE9HpoPwTf9JYL6aSnvSOCEgjKiE+Ij5GWAx1a+CJDL2fd7OAsmJLlxeHdH1mIOtaFAvRKZbc/QYyWfxhqey50zsiIBlhMXT6718++kQXna8em/LVhN+K1sk9pv/+JaKTHkSniCidnqSTnodO0hhWejq9e9L01Ak7FwbHt/Ro7KvyViM6P72Ll65p10dnnPo6aXoqdtXpQXSKjsYX3um8uZ/MpTEsK4GhwaOXpeUcPL7ptcUunm6OfGaaX55N/d38PZI/moYjnLQhOmm4fe2m6BtHVOaeMmmtJK6IjjGv7lnWfVqKe6CXdzMVdQnyCPZ1D/RKfHvMKzs/Q3TShuikhEbbDfHTU/63jBzR9ZmBr2WvaJ+aRP6zAqhgQi+V+AmDX8teweM5be4gOuk5/dN+0ccUPz1vX+fyrJL1dHr33i+kzDj1ddOuj7p46RS5GOrqo3f1dms5uPOMU1/3fiEFS5wS4D06y0ssso1OQojx5CXRxxR/3bPoslH0MWXIO9B/1Kcz8w056yYv0DhpS2/cZV2RaNwbeTdo1WTg7PF4T5cM19G5LGlaeYmlwlTGupb60DiBLn56yrAxHT1NoiJe2fmZITNrw8QPtS5OJQV831DyCPatLL835OMpPLai4Be/0WkxmZclTXNydZZ5dAryDTniTgjEf3MvOn9N9DFlLioh/rXDfPddRg9jVjyb+gdENu4zaQTrQmxmMZlXjE5zcnXmpbeO6IuK4s89b5+7LvqY8lfdamT7h6sM3+4hhPDSasTV202j1UY/3RMNPqTn6uMeENl4dPps7laWhegsOneVl+gkFBYVRZ570jiSypH/9l2Oa+7RmIMdefQwZsitgWfD2GaITslc2Hdc3AFFnnta7lL8ejIvhL7LQquRclNp8QU5HkLwbhbgonfrNzsV7+lMeIX4+4Y3GrNyDqJTMqZbxeIOKHJ6KuCGu1hqthqRVd9l9DBmDtHJhOi33UVOz7s3C8UdkGty67uMHsZygOhkyGIyi/jbLvbcc79B3AEVoFbf5QpzmfSHitHDWCYQnWwZLxSIeGhJ5PQ037wj7oCKUbPvsnuQt5Q9Q9HDWCYQnczdvn5TvumpyP4gIopKiI9KiN+7eos0fZfRw1g+EJ1yIO6hJTFPLFlM2HC3igR9l9HDWFYQnTIh7saMmOnJ+wc5pFSz77K4rUbQw1hueI/Oa0cuKCM6idgbM2K+uZeWyLfDijwJfZeFViNObi6mK7cdHFD/iI8+yBs9jOWD6+hcmTr72pELZbeV804p7saMmHNPGv1H1UBoNRLWK8bV282RcXS++rBeMehhLB/8RichZGXq7JunLyspOonYGzNUesuDHVw99c4eOs+mdh7D9Gzq7+Tu4uqpwGajnPIK8b9XVsFpdGbMS795+rI6P0JjPTHTU/RrpGrT8/URMcN72hGg7o28Y4b37Pk6f316lMqtgee9sopxGQs4jc7j3+xWanSK2ItDzPQU/RqpCiVNT+0+LUXnq3f1sWoW6eqj1/l5JLzxDI/dIZXKWe+q0WjGZSzg8WKCsqOTiNqLQ8xdIxyVF0XXZwaGto1cN3mB2ehKNORBHZf1jbw1Wq1/y8ZoAi8rOj+91tlp/Lb3EZ3yJOLmtpjpiaPyYhH2kXIOHj+z+9CF305c2Xe21k8I7t4ytFNUm6QeyE1ZQXTK37WzeWJduqPyPXcQRUTHmIiOMWQ66zrAOohOtRFt3bPYiN93UC9EJy+u/Zkr1lDiped1VfzWA9wP0cmRG3+K9mlinPcEcAiiU7VES09c0wQVQnRyR8SjQaLtGuGaJqgN79F5ZPn20ht3WRciNRGPBmHPHcAevEfnwcWbK0zlrAvhG9Y9AWzGe3RmL9uG6HScaOmJ78GBSnAdndmbdmUv22YpUvUuhVh93EVLT3wPDtRA56e3FJqGfPoKj9FpyMzKeHWJyqOTiNfHHW/uADawFJpGrEuLSohnXYjNDJlZ68cuQHSKCOkJYANEJ1TDnjuAVXS++qGfT0N0QjXMPQEeDtEJ9xNv1+jnE2INBSAriE6FyT16WpRxMPcEqA+iEx4E6QnwQIhOqAfSE6BuiE6oH9IToA6ITngonFgCqI3r6FyTPId1FWqBuSfA/0B0gpWQngD/xW905hty1iTP0fnpWReiIkhPgH/T+eq7ThvGY3Qacwu+HDZL6GDCuhYVQXoCEEKIi5cublz/3i+ksC7EZsbcgqX9p1ZW3EN0SgzpCUCc9S4dJiQlTU9lXYjNEJ0MYc8d1M6zqX/M8J6ITrAV5p6gaohOsBvSE9QL0QmOQHqCSiE6wUFIT1AjRCc4DukJqoPoBFEgPUFdEJ0gFpxYAhXhPTorzGXldy2sa4F/Q3qCWvAdnY9PLS+xVJjKWNcC/4U3d1AFfqOz2HhrWdI0ZzcXRKfcID1B+Tyb+rd4vAOP0Wkxmde8+J6Tq/OdvFusa4HakJ6gcJ5N/QMiGw+aNZZ1ITazmMwrRqcVnbuK6JQn0dLT1dtNrKEAxOLq4+4X0Wh0+myd3p11LbZBdFKi0WrdvMTpgipaej4S30KsoQBEoX/Ep2FsszEr5yA6oVpVZWXD8BBRhsKeOyiTV4i/b3gjRCfQg3VPUCBEJ0gA6QlKg+gEaSA9QVEQnSAZ0dIztHOUWEMB2AfRCdYIbBYsyjiipadngJ9YQwHYAdEJVhLr3xDsuYMS8B6dN08XmK7cZl0L2AbpCdzjPTqvHblQdtvMuhawmWhv7r6NAzVO2IMCqXEdnStTZxfmXEV0SskrLECsoUTLO5+ggKp7lWKNBmANfqOTELJj8Zqbpy/fvYS1Tkn5t2gs1lCYLQKvvEL875VVjPj0DR6jM2Ne+vFvdiM6uYZ1T+CSs961orR8/I/vewf6s67FZohOZRAtPZtERYg1FED9XDx1zu6u4398PzBUnIN7UkJ0shU1sJtYQ2HuCZzR+em1zk7jtyE6gTGsewJPEJ0gH2KmZ2jfaBFHA6gF0QmOC20bKdZQmHsCHxCdIDdipqfe31vE0QCqITpBLDpP0c63iZmezbrEiDgagADRCSIS8d8ivLmDrCE6QbbEPLHUsIU431oCEPAenQcXb64wlbMuBP4rKDZMxNHEnHu6eYjznU8aVjw5c+/qLayrUDWLybx39ZZdc74uLbxrzc/nPToPLclAdMqNe4CXiKOJOfcUcTlWXCUFRYSQfZ9uyFq2afD8SREdsT4rNUNm1k+z08tNpaU375befHh6ch2de1dvyV62rfyOhXUhUJu4O9tipqfM/0UvOnNV56f/7vm5wZ1aDpiZKvNqFSPfkLNz0ZqCA2dKLhdZ+Ut0fnpLoWnCnkU8/jMyZGbtfGulpcjEuhCog7g72+q6qWkpNFkKTQVZZ5b0nhI3rv9jY4bw2GOCF8XGW7+u2JC9bFtVZWVZcan1v9BSaBqxLo3HzgmGzKz1YxcgOlVC5D13Lq4blRQUWYpMJ77dvajbhL2rt1hM6E0rMmGJc26rUSe+3W0pMtkUnYSQEevSohLiKdVGD6JT/kS8aETUNvesSfgC128Lv8tatqnf7FQe/7jKkyEza8PED7UuTuQ/v8nW0/nqh34+jcd/FohOFRI5PaMGdsv9+YS4Y1JVfOEmIWTjyx8d7tSy98sjeHxblI98Q86W2UtvnMo3X79jxy9HdAJt4v4BV+/cs6aSy0UXdxxbvusEFkPtU2y8tf3DVYZv9xCNtuy2PSGC6ATuiL3uKeqygpTKikuFxdC5rUZhMdR61UucZzbtLysuRXSCbIm+K4Obmv9DWKfbM++b+e3HGDKzWJcjd9mbds2PG7Nn3jeEENPVYvsGQXQCp0R+c1fGuqFwun7DSwt/bdVk4Ozxyvg/Ja58Q866yQtKb5WYjfYscVZDdIJkRPwmhwDrng9kvlp8zXwxfdCMqKd7JL4yEouhgmLjrY1vLTn3Y7bW2clS6FB2IDpBMhqt+O/Z4o/IxZFPK5XdNpUVl57ZtH9uq1E7P1ur8sVQi8m887O1c1uNurT3ZPkdi5qjc03yHEQnX6oqK0XflRE/PZXXI1lY0TucnjE/bkz2pl2sy2Fj7+ot8+PGHE7PIP9Z2XAE79HJugqwh+iNOMRPT6X2SC6+cNNsvLP9rRUf9n4h35DDuhzp5Bw8/kGPcb8sWGs23hGOxzqI3+jMOXh8TfIcnZ98e4lBPURvmyD+uqdv40DRx5SPu5duld8t/WLg9PDH4554e4KyF0ONuQVb300vOHCmwlzm4Ht6NX6j05hb8O3ofwodTFjXAjbzCQ8SfUzx09MnKED0MWVF+MNzae/Jua1GdZn+ZJ9JI3R6mbbms5vFZN6xeE32sm3OHq7W90Z6KJ2vPm5cf06jc2n/qZUV9xCdnPJt3lD0McV/c1fJ+R5h7e/kxn3z2v1NYX2X967eMq/d305u3GcpMjm+xFnNxcM1blz/pOmpYg0oGUSnAoh+XIlQOrHk6u1ma1sdThWduUoU1HdZ6GF8r+KelT2Mreesd+kwcSCiE5jQaDVuXuKvVlNJz0fiW/DVK8RBCui7bEcPY+t5NvWPGd4T0QmsVFVWNQwX/6trVG5qhnaOojGsnFkKTSWXi4S+yxnz0ouN3HxGsdh4K2Ne+vIn3ri44xiisyZEp5IENhN/TkNl7tkgLFij1VZVVtIYXM6qF0OPpG/vlTaq/ZDect5QspjMhzfs3DXnaxcPV0pnvxGdIAeu3m40/iRSSc+G4SEqjM5qwmKozPsu/+9n2qg8AtEJMvFIfAsaw1JJTxqTZO7Itu+y0MP41pnLNN7TqyE6QT4orSVSSU+d3l092+71k1XfZcd7GFsJ0QnyodFqG4RRmc/R6u9JaarMIzn0XRalh7GVeI/Oe5ZyRKeSVFVW0thwJ/TSM7xHO0ojc4ph32VDZtb89o72MLYS79FZXmLBO5PyUFpLpNXfs1HLMI2TtuqeeveO6iRx32Whh3HJtdv2fabNVlxH57Kkac7uLg42ewYZ8goLoHT0hVZ6+gQFIDofRIK+y9U9jDVaJ6rv6dX4jU6Lybx+2kInV2dbv58MXAh8tCmlkWm9uctni1me6PVdrtXDWLLobNI5ktPoXDE6rejcVUSnUkX260xpZIpfhQuKDaM3uDIIq5BZSzbNjxtTdPGK4wMWXbwiYg9jK7k18AyIbPzUgleleZyIEJ1q0LAFlS0jQjU9m3Z+lN7gSlJSUGQ23im5VnTFcN6Rca4YzhdduC5WD2Mrufq4B0aHjE6fLedbVXVCdKpEULMmlEammJ6hca1ofIlJqYxH887+eChjXrp9vzxjXvrZHw8V/XlV3Krq5xXi3zC22ZiVcxCdIE+u3m70DllTTDeV39e0w91Ltw4u3mxHgGbMSz/+ze67lyQNAq8Qf9/wRohOkDOqB88pfpEYG0d2qDCVH/9m962LV59a8Ko1qWQxmb+b9kH+/tOITishOlWFRlPkanTfrLFxZIe7l25dOXxWaFlfT6e7YuMtoQn8lcNnEZ1WQnSqDb0tI0J17kkIadr50etHLlJ9hCLdPm8khOz7dMPOt1bqH/FpGN2scUyEm5cHIaT0Tsnl4znXTlwoKSjUP+IrehP4h0J0AkfobRkR2ukZGtfqiHYbVj/tI3S6sxSZCk9dOf3dvvt/QlmxpHtEBNEJXKG6ZURov7lj40hJEJ3AlybdIqmOT3fuiY0jxeA9Oq8duVB2m0F3K2CI3i0jAfXzmKF9o2k/AmjjOjpXps6+eboA0alCoW3pzj3pp6f6vhCnMPxGJyHku2kf3Dx92XTlNutCgAHaH7mgnp7hndrQfgTQ4xXir/Pz4DQ6M+alS38SFmQiKDaM9r+01NOT6okBoMorxP9eWcXI5X/nNDqlv38F8hHWPYb2I6inp3egv1dYAO2ngOic9a4V5vJxGQsCQ/n7xh+iU+U0TtqIrm1pP0WKLh5/SZLjJ3mhHq4+ehcP3fht7yM6gUdV9yqbtqb+aTUp0jM0rpXGCc2WuKHz0zu5OiE6gV86X70E36+VItRC2rTEVzp4ofPTa50RncC35v2k+CqlFOkZGBrs6u0mwYPAQYhOUACNVtuqXycJHkT3rlG18MfjTq3dK82zwD6ITjkLS4z2a9a4cVT4/X+rsOBa4cUreb+dlOxbLDJXVVkZ0qalBA+SKD1b9et0et1+3HmXLUSnDIUlRkcNfCykbcsmj1p149mYd/nSsTPZ3/x0cfsJ2rXJmau3mzT/GkuUniFtWiI6ZQvRKTddZgztmNI/MKSxTb8qMKRxYEjj2EEJ+Sdzdn+y9tTaOvrEwjdiAAAfuUlEQVRyqUH443HSPEii9BSWPsuKS6V5HFiP9+g8uHhzhamcdSGiaTe+X+Iro7wb+DkySJNHI0Z+MvNI/8xts75Q2+u8ZIueRJpdI4Fk/0EA6/EenYc+2aKY6PQI9p3wy6Jh7052MDqrxQ5KGLt5vkewryij8UKyRU8iZXq26tdJo9VI9jh4KK6jc+dna7OXbSsvKWNdiDjCEqOnHUi3cn3TeoEhjdUWoJItehIp0zOkTcuqyirJHgf14zo6DZlZexd8bykysS5EHGGJ0aPTZ7u6UznVFxjSuP87z9MYWZ5aDJbuZqN06RkYGqzz1Uv2OKiHzk9vKTQ9vfJNTqNz/dgFiolOj2BfetEpiB2UoJLpp8ZJ27JXe8keJ+kFytbP9JTycfAglkLTiHVpER2pN6ERncKikxCS8sXrVKNTED/hCdqPkIOqe5UtOlNvDlJN0vRs2VO6/yxAPUasS4tK4K91i/Kis1VKl/AOUnx8oVHLUAmewpxXWIAE19urSXRiSSBB1xOon85XP/TzaYhOmWg3rI80D/JpqIouka3+2lXKx0k69/QO9A+KDZPyiVATolNuWuDLC6KKSqT7GbhapG4cFzlQooOsUAuiU27CEqMlWPFUFYnfbqVOT3zmiAlEpwy5+3lJ9qy8o2ckexYroX2jJf6EjNTpyeM+L+8QnXDZcI51CXRptNq44YkSP5RBy/dWKZKu7KocohMIIX9uyWJdAl1SXtCsxiA92w3rjQ91SIPr6FyTPEfZ0WkuvCPNgwyZWYrvFeIVFiD91Q8GKda0dQt8qEMCvEcn6yqou7j9RJlZiq5jO95bKcFT2GLy6UkG6YlzSxLgPTp1fqq41Hv2wDHaj9i3JuP6kVzaT2EuJukx6R/K5g269ZPdmTxXJfiNTmNuwYYXPxSu4bOuRQq/f7+D6viGzKyMyZ9SfYRMMLmJwyY9Yx7vxuS5aqDz1Sd9MIHT6Fzaf2plxT2VRCch5NTafUc2Z1IaXCULIISQVildJT6rJGCTnui3RImrt1vcuP5xg3uxLsRmKoxOwfoxC4x5l0Uf9sjmTJVEp8ZJ225YbyaPZrb33eZvEt3wVQ9nvUv7FwYkTU9lXYjNVBudgs8HvWbIFO1EUfGNwlUT310/ZoFYA8pc1b1KVg00mKWnxDdSFc+tgWfHSYMQnTwqKShakzzn+5kfFd8odGSc4huF+9ZkzI0cqarvwQXFhknZV6kmTVUVs37vbzcfiu/EicKzqX/M8J6ITgXoMmNoZM8ONrWtKzOXXvrj7Ondh/bNXU+vMHnSaLVDvniF1VIVy/RcM2WeYdUeVk9XDESnIrVK6dK8a1ufRxoIzeV0nnrhA8X5J3OEn3D93KXCAuOVE2dVNdO834xTX6tx7qmePUF6EJ2gZj7hQdOzVrB6OssbkxHx6BjiEEQnqJlGq40b059hASzTU6d3R8cQuyE6QeWqKivZnhxn3K2D1UEt3iE6AZh0BqlJ0u8a3Q8v73bgPTrLSywVpjLWtQD32j3bl20BjOeeeHm3FdfRuSxpWlVVFaITRBH7BOM7dez7bOLl3Xr8RqfFZF713D+cXJ1Lb9xlXQsogU94ENvXdiKH9MTLu5W4js4Vo9MshSV38m6xrgWUgPluu4B9eur07lEje7CuQu48m/oHRDbuM2kE60JsJkRn0bmriE4QC/PddgH79CSEdBzB/j8jcubq4x4Q2Xh0+mwmbbgcgegEGoJiw5i/thOZpGdExxhXb3zYum5uDTwbxjZDdAIINFpNt0lDWVdBiEzSkxASPYq/lpQS8ArxD4wOGbNyDqITQFBVWdWic1vWVRAin/Rk8lkSmfMK8fcNb4ToBKjpkS4tWLUFqUUu6RnRMcYrLIB1FTKC6AS4n8ZJm/DKcNZV/Jtc0pMQ0u7ZvhqtjOphCNEJUKeqe5XyOeMoo7SKfaJXVSW+847oBHigqJE95PPnQkbpGRgajO+8IzoB6iGr042Mu4TU0m3S0A1jP6y6p9IZKO/Ree3IhbLbZta18C0sMdqvWePGUeEhbVsSQpo8GlH9t4QvcFzMPpW1ZGNJQRG7GpnR+eojOsrltZ2w7S1/P4vJPCdkGOsq2OA6Olemzr5y8Byi0z7CRzhC2rYMatbE1f3hB5/LzKW/rty0a9ZKCWqTD41W+9isp/pNHsW6kP+SV3oStX7siN/oJIQsGz7j5unLdy/hhd0GHsG+bUb2juzZoWnrFtYk5v1U+GEbhp8wqpO83twJIR1H9FdbenIdnRnz0hGd1guKDW39ZM+YAd2ET7w5IiohfuiKaer5bnuj+Oayik4iw/QUDn7euXiTdSES8Qrxv1dWwW90Hv9mN6LzoYSZZpuk7jXXMR0XOyjh19h114/kijimPGmctL2mjWRdRW2yS09CSOeJf/15xgo1nF5ya+B5r6xiXMYCRKdStUrp0m5Yn6iEeErjt36y564jyl8AdfFwlc8xz2pyTM92A3tufy2ddRXUOetdNRrNuIwFcugWYytEZ/08gn3jJzzRYVhf7wZ+VB/k7u1BdXyZiB7VS4YzDDmmp3egf/MBbc9vPcq6EIp0fnqts9P4be8jOhUmKDa0zxujW3RqY99eENTpsef+yrqEOsgxPQkhncYMVnB6IjoVqVVKl85/GxzeIZp1IUojh49w1Emm6RmVEK/z1VuKFPjRWkSn8nSZMVT0HSEQaJy0Sf/3Ausq6ibT9CSE9Jg5XHl7R4hOJRF20h8bM4T24mY9CguusXq0NJz1LjLcLxLINz2Vt3eE6FQMj2DfnjNGtB/Sm/niZuHFK2wLoK1daj8Z7hcJ5Jue3oH+USN7KObkPKJTGYJiQx97Kbl1n87Mc1Nwau0+1iXQ1WXUQNYlPJB805Mo6N4R79F5cPHmClM560IYEzbT6Z3ctEP+yRzWJdAV2jdazn9kZJ2eER1jfMKDbp+7zroQhyA6eSfD3BSc+eUI6xLo6jpuCOsS6iPr9CSE9J45iuuedbxHZ/aybWqOTpkfQjqv6PTU+epl+F+smuSenq37dN6sX1x+x8K6EHtwHZ2GzKzsZdsUeWjMGq1SuvScmCLnQ0jGvMsXt59gXQUtGq2m99ujWVfxEHJPT53evV1qv4MLN7EuxGa8R+f6sQvUGZ3yz03B8a2/sS6BoqrKqujELqyreAi5pychJGF8MnfpqfPTWwpNI9alITo5wktuCv74YTfrEiiKmzhAbv3o7sdBenoH+ocPjju3KZt1ITYQolPmqzZ1Umd02pebxrzLl46duXL6gnDosnnXti26tXO8cac18k/mKLsxnTwvttfCQXoSQhKnPruEq/REdPKiy4yhHVP62xR5xrzLx7f+9scPu2vl16m1+zyCfacdSJfgKOixjF9oP4IhmR9UqsZHejaJivD9S6OiP6+yLuThdL76oZ9PQ3TKX5cZQ226ZFl8o/DQ9z/fH5o1lRQU/bFjf+ygBJFqrFuZufTYqp1UH8GWzA8qVeMjPQkhA94dJ/+vuCA6uWBTbpaZS88eOLbv8w1WbnCX3qH+e3j2wDEFf1PTKyyAlz9B3KRnVEK8zL/YgejkwozTq6zMzeIbhb+u2HBs1U6bosrnkQb2lmat37/fQfsRDA2aP5F1CdbSsi7ABo+98pTGSaYFIzp5cej7nx/6c84dOrFq4rtzI0fum7ve1lle0+i/2FuaVYpvFCr4brvOVy/bjkr3k2kY1an9kN7OehfWVdQB0cmRXbNWPuh6eJm59MjmzEWJLy5//HX7EiooNpR2tzpr0p9Twgl52XZUuh9P6anTu3d+ZYhGK6+auY7ONclzVBWdgvVTPigzl9b8keIbhTs/+25Bp9T1YxY4chIoom97h6t7iKwlG2k/ghVnD9f2Q3qzrsIG8kqih+o8PElW/ZJ5j07WVbBx/UjupneWCX9dfKMwY/7yuZEjd81a6fhWTFj7KIerq48hM0up+0UarVbOrTzrxM2ukcA70L/jlMEyuXqE6OTX70t/ahwVfn7vUXHXEFt0aiPiaPc7tSOL6vgMVVVWJoxPZl2FbTibexJCZPJbzG90GnML1iTP0fnpWRfCWMbkT8WNznbj+1E9J198o/D3pT/RG58tLq5m1sJfenoH+sdNHMC2Bq6jc2n/qcI1fNa1KE3zTnQb2f2xXbFb7YSQPpOGsy7BZvylJ2H9G63z1XedNozf6KysuIfopCGic1uq4x/6MoPq+AzxOPEknKan0DeEyaNdvHRx4/r3fiGFydMdgeikKiwxmupZJUNmloLbgnDRE+R+XKYnISRx6rPSP9RZ79JhQlLS9FTpH+0gRCdtccP7UR1fwfeLwgfHcdET5H68pmeTqAiJp5+eTf07ThqE6IQ6te7Tmd7gyr5fxGQmJApe05NI+5vu2dQ/ZnhPRCfUifZuu4LvF4UPjmsSxUc76vtxnJ6STT8RnVC/Vn3obiEq+H4RvxNPwnV6Ekl+6xGd8FBUD8kr+H4R1xNPwnt60p5+IjrhobrMGEr1tV3B+0VcTzwJ7+lJaP4DQHSCNSJ7dqA3uDHvslL3i6JG9uB64kkUkJ5NoiJoXD3iPTorzGWITgkExYaGd6B4xejg2m30Bmdr4MznWZfgKO7Tk1C4esR1dC5LmlZeYim/a2Fdiyq0frInvcEV/P0iTi8X1aKE9BRuvovV95Pf6Cw23lqWNM3J1bnCVMa6FrWIGdCN3uAK/n4Rj7fa76eE9CSE9Jk0XJS+n/xGp8VkXvPie06uznfybrGuRS3CEqOpfr19x3sr6Q3Oikar7ThlsAImnkQx6ekd6N897WmNVuPIIJ5N/Vs83oHT6FwxOq3o3FVEp5S6jKX44dz8kzmKvNju7OEikyaTjlNIehJCej4/zNnD1e5f7tnUPyCy8aBZY0UsSRqITlaoHvM8lvELvcFZ0Wg1CWkjlTHxJEpKT53ePSFtpH0f3XT1cfeLaDQ6fTZfHwYgiE52qB7zLDOX7pu7ntLgDLl6u3dKeZx1FaJRTnoSQjqlPO7qZfO/0PpHfBrGNhuzcg6iE6xH9ZjnHzv20xucoaQPJnD3p6weikpPnd596OfTbPolXiH+AZHBiE6wCe1jnr9+vI7e4Kz4hAfFDe7FugoxKSo9CSFRCfG+f2lk5U/2CvH3DW+E6ARbdfhbEr3Bzx06ocj9oic/foV1CSJTWnoSQoZ//oY1Pw3RCXZrndiF3uC//yuT3uCshPaNjugYw7oKkSkwPa1pHYLoBLu1G9+P3kc4lPrhzAGzuL+XeT8FpichZNjcKfX8XUQnOIJqN0/lfThTo9XGTRzAe0OQOikzPes5PM97dBpP5CE6GfII9qX6OVXlfTjT2cNFGfcy76fM9CSE9Hx+mIunrtYP8h6d145cKL1xl3UtqhY/4Ql6gytvv0jjpFXS8fhaFJueOr37wIUTa/4I19G5MnV2Yc7Vsttm1rWoXYdhfekNrrz9Iu+wBko6Hl+LYtOTEBI3uFej+ObCX/MbnYSQHYvX3Dx9+e4lvLAz1iqlC739ojJzqfL2i578+BUe/8RZScnpSQgZMu9lwnl0ZsxLP/7NbkSnHLQb1ofe4Mq7X9R8QFvlnVKqSeHp2SQqovmAdnfybo349A1EJziC9n6R8u4XJb8/lXUJdCk8PQkhye+/6hXqf4LDgyCITlmhul+ksH50Gq0mcX6qUjeLqik/Pb0D/Vun9Nw15+tiI08xhOiUG6r7RQrrR+cZ4q/gzaJqyk9PQsjA6amewb7bP1zFuhBrITrlJiwxmup+kcK+XzTs02k8LpTZShXpSQj56/zJhm/35BtyWBfycIhOGaLaRl5h3y8KHxyn7M2iampJz2ZxUc37tfvuxXkWk6yPTCI6Zcgj2JdqG/lTO7LoDS4xFy9d/feklUQt6UkIeer9qRWl5Yc3yPcVCdEpT21G9qbXRl5JbUE0Ttq+7zyn+M2iaipKT53ePeH1Z7a+vMSYW8C6ljogOmWrTVJ3eoPn7D9Kb3CJNWwf1vWZgayrkI6K0pMQ0mFIn0e6tlg/bSHrQmrLmJd+ZPl2RKcMBcWGNnmUYn+g7G8UMvEk/7mcoh7qSk9CyLNfpBXn3cjetIt1If+VMS/94OLNaP8hT1TbyBffKLy4/QS98SWj0Wq6pz2tyDZ09VBdenoH+j86tNvW15bK5Phnxrz0w59trTCVsy4E6ka1jfylE3/SG1xK3s0Cez4/jHUVUlNdehJCBk5P9Wjks2HmYtaFkOxNu7KXbSsrLmVdCNSN6jFPIupuu0ewb693RgfFhoo1oE2U3Q3kQdSYnoSQlKWvFxw4w/b93ZCZlfHqEkuRiWENUD+qxzwJIaLstgfFho5Yl/bmsdW9X3hqxBezPIJ9HR/TehqtJmZMb5Uc8KxFpekZHNk8KqX7jzOWsXp/N2RmrR+7ANEpc1SPeZ475OiKZ7vx/Sb8sujl7Z9Wty8JDGn8xMLJDpdmAxdP3V/fniDlE+VDpelJCHli5njvkAYb31oi/aMRnVxoN74fvWOehJBrZ/Ps+4XCS/qM06uGvTv5/vMAUQnxXWYMdbg6az3z7VsqfGcXqDc9CSFDF7166beTEr+/Izp5QfXrb4SQ83ttPukZlhhd/ZJez4Js30kjwhKjHavu4TRaTdTIHup8Zxc4sy6AJeH9fetrS1t0bivNBQlEJ0eovrYTQvJ+O2nlz/QI9m0zsnfHlP6BIY2t+fmu7m5xw/vRPgvl6qMf+s+XqD5C5lSdnoSQJ2aOP7/zyIaZi0cvS6P9LEQnR2i/thNCQro9emrtQ9rOtkrp0m5YH5u6MuefzNn9ydqHjuy4EatnqfadXaD29CSEjFyRtuKpWXtXb6F6yQzRyZfmnai/+facmPKgjAuKDX3speSIzm1tOi9lyMza9/kGCY7fa7Sax2alqPmdXYD0JIGhwR3HDtz68pK/dGsXGBpM4xGITu5EdG5L+xFNHo1I+ujFQ19mVHeVD0uMbt49NmZANyvf0KsZMrN2vLdSsu706jwbfz9NVVUV6xpkYVHiRJ2PnsaX4xCd3AmKDX15+6eSPc6Yd9ly1xTUrImtawVl5tLDG3bunrtG4vagE/YsUtulzDph7vlvY1b/47OBU3/7alPvF1JEHBbRyaPgDpFSPs7WmSYhpPhG4a8rNhxbtVPi3NQ4afv+3xhEpwDp+W/egf79/5G64YUPQ2NbibWgY8jMWpM8R5ShQEqNo8JZl/BA+SdzjmX8sm/ueiZPbxQf3mPMk0weLUNIz/+KSez2x6C9347+52vZKxx/f0d08qthixDWJdTh3KET+7/cJMFm+oO4eOmeTad+NIUjqj4tf7+h7012C/D8btoHDo6Tb8hZkzxH56cXpSqQmM5DRgdxysylhsysRYkvLn/8dYbRSQhJXj5DPX3jrYH0/B86vfvwL968fPjs3tVb7B7EmFvw5bBZOj+9pRDLnVzyDgpgXQIhhBTfKNy3JmNBp9Q1yXPYfu1duFZk07FTNcCbe23Bkc3jxw3aOfur0LaRdqyOG3MLlvafWllxD9HJL6pd6azBdnHzft7NAlV+rahOOLFUt89SppuuFk38cZFNC6CITmV490YGq0cbMrN+/34H2zf0+03JXkbpKDTX8OZetzEr3i43l21+53PrfwmiUzGMeZclfmKZuXTfmoxFiS+uSZ4jt+h8cvlURGed8OZeN53efeRXaauenbM3yqobnIhOJbHcle4fojHv8sG12+Tzkl6TRqt5dET3uMG9WBciU0jPB7J+ARTRqTBnfjlC9TuahJAyc+nZA8ekuZZuNyx31g/rng/xxcg3r2afr+cEKKJTeaje1BQmm9JfE7IDljvrh/R8CIvJ/HHiS56P+L2wbv79fxfRqVRDV0yLHZQg4oBcTDZrGrEuDUeU6of0fDhjbkH6k693GDuw1hV4RKeCeQT7jt08344b6Pc7d+jE6d2H5LmyWSeNVtNh8qAnZo1nXYjcIT2tcmjDjq1TlwxLn179X2NEp+J5BPumfPF6eAc7G30KocnFG3otj3RpMfbb91Te+dgaSE9rrZ78f+d/+v2F7R8EhgYL0XnPUo5PsSteu/H9eowfZuUktPhG4aUTf148bOAxNAWu3m6vZH2OG5nWQHra4MNeL1Tdq3zq0+lfDptVXmKpMJWxrggkEpYYHTXwsYYtQu6/An/72s3bV25cNpwrOHSa7X1KUaB3p/WQnjawmMyLer54+/x1rxD/O3lsPgQPQM/gJS/FJ/dnXQU3cNfIBjq9+zNf/d1J54zoBIXRaDUdpwxGdNoE6Wmb4MjmKaveZF0FgMgadYro/+qzrKvgDNLTZlEJ8d3TnmZdBYBodL56bLLbAelpj36TR0WN7KHRalgXAiCCCTsXIjrtgPS009B/vtSoE7YmgXsj1qXhOqZ9kJ520undn01P0/ni2xvAscT5qbiOaTekp/28A/0n7Fzo4qVjXQiAzYRNdnwg0xFIT4cEhgYnL5/BugoA22i0mkadInCT3UFIT0dFJcSPWIfPtAJPGnZoNvbb91hXwT2kpwiiEuI7ThnMugoAq+h89U9/+jo22R2H9BTHE7PGx00cgDNMIHMuXroJOxdik10USE/RJM14rlGnCAQoyNnItbMRnWJBeopGp3cf++17OAQKsjViXVpExxjWVSgHeiyJzGIyf9h9/J2LN1kXAvA/8KUN0WHuKTKd3j11/Xs4RQ+y0nHKYESn6JCe4gsMDZ6wcyECFGSi45TBONpJA97caTHmFnzSfVJ5CfrPAzMaJ22HlwYiOinB3JOWwNDgkeveZl0FqJdGq4kc1hnRSQ/Sk6KIjjG4hgRMCHcxk+e/wroQJUN60oV7nCA9ITrR8Jg2pCd1CFCQEqJTMkhPKSBAQRqITikhPSWCAAXaEJ0SQ3pKBwEK9CA6pYf0lBQCFGhAdDKB9JQaAhTEhehkBenJAAIUxILoZAjpyQYCFByn0Woik7sgOlnBPXeWjLkFn/R8qfyOhXUhwB8nZ6e4SUm4iMkQ5p4sBYYGT9z9MboxgR0QncwhPRlDOzuwA5rOyQHe3GXBmFuwZuw/jUfzqiorWdcCcpf89Yy2j3dnXQUgPWXDYjJ//vQbVw/kVFXinwg8ED6wIR9ITxmxmMyrXnjnwk/Hq+5hBgq1uXjpRq6djc+6yQfSU3Y2vrP04MJNrKsAedH56vEddrlBesrRnhU/bH8tnXUVIAsaraZhh2ZPf/o6olNukJ4yZcjMWpM8h3UVwBiuEskZ0lO+8g05y594w1JkYl0IMIOTSXKG9JS1/5xkysVGvAolzk/tMeZJ1lXAAyE95Q4b8Srk4qVLXj4DJ5NkDunJB2zEq4RGq/UM8Utd/x72iOQP6ckN7CMpnsZJ2yg+HHtEvEB68sSYW7Ck9xTsIykV9oj4gvTkzL8vdGadwzKowuAKJneQnlzCMqhiaLRa72YNxnz3DhY6uYP05JUhM2vdc3PRWZl3zQe0HfnZLCx08gjpyTGcBuUdTnRyDenJN4vJvP7Njw2r9rAuBGyg0Wpdvd2e2/hek6gI1rWA/ZCeSpC9adfmlxfjLZ4XeFtXBqSnQhhzC7598f+uHbqAt3iZw9u6YiA9lcNiMu/+4vtf5nzLuhCog0ar8W4WiL11JUF6Kk3OweOrn367/G4ZPpEkK1Ejewz950t4W1cSpKcCCY1Fzm89yroQIIQQV2+3Z759C1/UUB6kp2JhK0kOmg9om/z+VO9Af9aFgPiQnkpWbLz1VeqcK/vOsi5EjVy8dIMWTYob3It1IUAL0lP59q7esvXlJayrUBdMOdUA6akKxtyCTX//FCuhEsCUUz2QniqClVDaMOVUFaSnuhQbb62b+j4moeLSaLUunq4DF07ElFNVkJ5qZMjM+j51XvldCy4miQJnOdUJ6alSFpN52wdfoUmoIzROWu+wBiOWz0SzD3VCeqpaviFnw/RFV7POsy6ES7ixrnJITyDZm3ZtmfIJLndaL3xw3LC5U7A7pHJITyAEL/LW0ThpfcKDhn/+Bl7VgSA9oSYcC30QjVbr7OHS953nuj4zkHUtIBdIT6gt5+DxH176sPjiDXy2s1rHKYP7v/osdtWhJqQn1G3v6i07/r4Cp5qwxAkPgvSEB7KYzAfW/rj9tXSNVqvCDaXQvtEDZj2PJU54EKQnPESx8Vbm0nWq2lDy/UujIQtfRkdOqB/SE6xSbLy1Y/E32Z9sZV0IXV5hAYPmT4xKiGddCHAA6Qk2UHCGIjfBVkhPsJnCMhS5CfZBeoKdFJChyE1wBNITHFK9p8TXvnyj+Oa9po1EboIjkJ4ggmLjrd+37N79j9XlJWUyP2PffEDbfjPG4BwSOA7pCaKxmMx/7Nj/85wv71y8ybqW/yHMi+MmDnjsub8GhgazLgcUAukJ4jNkZu1dtiH35xOsCyGEEJ2vvsfM4e0G9sR9IRAX0hNoMeYW/Lr8X8e/2llhKmfyOo/FTaAK6Ql0Ca/zO9/9+va56xI8TuOkrbqHl3SQAtITJJJvyDn43U/Zn2wVAo7GI3zCg3rPHNW6T2c0QwIJID1BUsJU9LfF668fuSjWmK7ebm2fS+wyaiAmmyAlpCewYcwtOLJxV9ZHmyxFJjt+uTCBbZXStd2w3ljZBCaQnsBYzsHjxzN+PfH1rrLi0of+ZOHsUVBsWLdJQ1t0bottdGAI6QlyYcjMOrZxj2HVnvv/lhCawrImQhNkAukJ8mIxmXOyjteMUWGmGdKmJZY1QVaQniBf+YYc7yB/zDRBnpCeAAD20LIuAACAS0hPAAB7ID0BAOyB9AQAsAfSEwDAHkhPAAB7ID0BAOyB9AQAsAfSEwDAHkhPAAB7ID0BAOyB9AQAsAfSEwDAHkhPAAB7ID0BAOzx/5iGh+dvmo3wAAAAAElFTkSuQmCC"


def logo_header(title):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.25rem;">
        <img src="data:image/png;base64,{LOGO_B64}" style="height:2rem; width:auto; flex-shrink:0;">
        <h1 style="margin:0; padding:0; color:#13405a; font-family:Georgia,serif; font-weight:700; line-height:1.1;">{title}</h1>
    </div>
    """, unsafe_allow_html=True)


# ── Snowflake session ──────────────────────────────────────────────────────────
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
    SNOWFLAKE_MODE = True
except Exception:
    SNOWFLAKE_MODE = False
    session = None

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ditteau · KPI Library Demo",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Design system ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    html, body, [class*="css"] { font-family: Verdana, Geneva, sans-serif; }
    h1 { color: #13405a; font-weight: 700; font-family: Georgia, serif; }
    h2, h3 { color: #13405a; font-weight: 600; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #13405a; font-weight: 700; }
    [data-testid="stMetricLabel"] {
        font-size: 0.75rem; text-transform: uppercase;
        letter-spacing: 0.05em; color: #7c776c; font-weight: 700;
    }
    [data-testid="stSidebar"] { background-color: #faf8f3; border-right: 1px solid #ddd8cc; }
    [data-testid="stSidebar"] .stRadio > div { gap: 0.25rem; }
    [data-testid="stSidebar"] .stRadio > div > label {
        background-color: white; padding: 0.5rem 0.75rem;
        border-radius: 8px; border: 1px solid #ece7da; transition: all 0.15s;
    }
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        border-color: #740049; background-color: #faeff5;
    }
    hr { border-color: #ece7da; margin: 1.5rem 0; }
    .kpi-callout {
        background: linear-gradient(135deg, #faeff5 0%, #ffffff 100%);
        border-left: 4px solid #740049; border-radius: 12px;
        padding: 1rem 1.25rem; margin-bottom: 1.5rem;
        font-size: 0.85rem; color: #13405a;
    }
    .kpi-callout strong { color: #740049; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
DB     = "DEMEAU_DD_DEV"
SCHEMA = "DISTRIBUTE"
MAROON = "#740049"
NAVY   = "#13405a"
BLUE   = "#4285f4"
GREEN  = "#5c861d"
TAN    = "#9a5a2a"
AMBER  = "#f2c845"
RED    = "#b8392b"
COLORS = [MAROON, NAVY, BLUE, GREEN, TAN, AMBER, RED]


# ── Helpers ───────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def run_query(sql: str) -> pd.DataFrame:
    if not SNOWFLAKE_MODE or session is None:
        st.error("Snowflake session not available. Run in Streamlit in Snowflake.")
        return pd.DataFrame()
    try:
        df = session.sql(sql).to_pandas()
        df.columns = df.columns.str.lower()
        return df
    except Exception as exc:
        st.error(f"Query error: {exc}")
        return pd.DataFrame()


def fmt_num(v, decimals=0):
    try:
        return f"{int(float(v)):,}" if decimals == 0 else f"{float(v):,.{decimals}f}"
    except Exception:
        return "—"


def fmt_pct(v, decimals=1):
    try:
        fv = float(v)
        return "—" if pd.isna(fv) else f"{fv * 100:.{decimals}f}%"
    except Exception:
        return "—"


def kpi_callout(kpis_shown: str):
    st.markdown(f"""
    <div class="kpi-callout">
        <strong>KPIs demonstrated on this page:</strong> {kpis_shown}
    </div>
    """, unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="background:{MAROON}; height:4px; margin:-1rem -1rem 1rem -1rem;"></div>
    <div style="text-align:center; margin-bottom:1.5rem;">
        <img src="data:image/png;base64,{LOGO_B64}"
             style="height:3rem; width:auto; margin-bottom:0.5rem;">
        <div style="font-family:Georgia,serif; font-size:1.4rem; font-weight:700; color:{NAVY}; margin-bottom:0.25rem;">
            KPI Library
        </div>
        <div style="font-size:0.65rem; text-transform:uppercase; letter-spacing:0.1em;
                    color:#fff; font-weight:700; background:{NAVY};
                    padding:0.25rem 0.5rem; display:inline-block; border-radius:4px;">
            Live Demo · DEMEAU Data
        </div>
    </div>
    """, unsafe_allow_html=True)

    area = st.radio(
        "Area",
        ["Admissions", "Registration", "Financial Aid",
         "Enrollment Management", "Cross-Domain", "Benchmarking"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown(f"""
    <div style="font-size:0.7rem; color:#7c776c; line-height:1.6;">
        <strong>Demo Data</strong><br/>
        {DB}.{SCHEMA}<br/><br/>
        <strong>Coverage</strong><br/>
        18 years · 2006-2024<br/><br/>
        <strong>Refreshed</strong><br/>
        {datetime.now().strftime('%b %d, %Y')}
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.caption("Powered by **Ditteau Analytics**")


# ══════════════════════════════════════════════════════════════════════════════
# ADMISSIONS
# ══════════════════════════════════════════════════════════════════════════════
if area == "Admissions":
    logo_header("Admissions")
    kpi_callout(
        "Admissions Funnel, Admit Rate, Deposit Rate, Overall Yield, "
        "Stealth Applicant Rate, Days App → Complete, "
        "Weekly Inquiry Pace, Class Profile Builder"
    )

    # Latest term funnel
    df_funnel = run_query(f"""
        SELECT
            term_code, academic_year,
            SUM(inquiry_count)              AS inquiry_count,
            SUM(app_started_count)          AS app_started_count,
            SUM(app_complete_count)         AS app_complete_count,
            SUM(admit_count)                AS admit_count,
            SUM(deposit_count)              AS deposit_count,
            AVG(stealth_app_pct)            AS stealth_app_pct,
            AVG(avg_days_app_to_complete)   AS avg_days_app_to_complete
        FROM {DB}.{SCHEMA}.MART_ADMISSIONS_FUNNEL
        GROUP BY term_code, academic_year
        ORDER BY academic_year DESC, term_code DESC
        LIMIT 1
    """)

    # Multi-year funnel trend
    df_funnel_trend = run_query(f"""
        SELECT
            academic_year,
            SUM(inquiry_count)     AS inquiries,
            SUM(app_complete_count) AS completed,
            SUM(admit_count)       AS admitted,
            SUM(deposit_count)     AS deposited
        FROM {DB}.{SCHEMA}.MART_ADMISSIONS_FUNNEL
        GROUP BY academic_year
        ORDER BY academic_year
    """)

    if not df_funnel.empty:
        row = df_funnel.iloc[0]

        funnel_stages  = ["Inquiries", "App Started", "App Complete", "Admitted", "Deposited"]
        funnel_counts  = [
            int(row["inquiry_count"])      if pd.notna(row["inquiry_count"])      else 0,
            int(row["app_started_count"])  if pd.notna(row["app_started_count"])  else 0,
            int(row["app_complete_count"]) if pd.notna(row["app_complete_count"]) else 0,
            int(row["admit_count"])        if pd.notna(row["admit_count"])        else 0,
            int(row["deposit_count"])      if pd.notna(row["deposit_count"])      else 0,
        ]

        admit_rate          = funnel_counts[3] / funnel_counts[2] if funnel_counts[2] > 0 else 0
        deposit_rate        = funnel_counts[4] / funnel_counts[3] if funnel_counts[3] > 0 else 0
        inquiry_to_deposit  = funnel_counts[4] / funnel_counts[0] if funnel_counts[0] > 0 else 0
        stealth_pct         = float(row["stealth_app_pct"]) if pd.notna(row["stealth_app_pct"]) else 0
        avg_days            = float(row["avg_days_app_to_complete"]) if pd.notna(row["avg_days_app_to_complete"]) else 0

        st.markdown(f"### Admissions Funnel — {row['term_code']}")
        col1, col2 = st.columns([2, 1])

        with col1:
            fig = go.Figure(go.Funnel(
                y=funnel_stages, x=funnel_counts,
                textinfo="value+percent initial",
                marker=dict(color=[NAVY, "#2f74e8", "#5585cc", MAROON, GREEN]),
                hovertemplate="<b>%{y}</b><br>%{x:,} students<br>%{percentInitial} of inquiries<extra></extra>"
            ))
            fig.update_layout(height=350, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Conversion Rates**")
            st.metric("Admit Rate",     fmt_pct(admit_rate),         help="App Complete → Admitted")
            st.metric("Deposit Rate",   fmt_pct(deposit_rate),       help="Admitted → Deposited")
            st.metric("Overall Yield",  fmt_pct(inquiry_to_deposit), help="Inquiry → Deposited")
            st.metric("Stealth Apps",   fmt_pct(stealth_pct),        help="Applied with no prior inquiry")
            st.metric("Days to Complete", f"{avg_days:.0f}",         help="Avg days from app start to complete")

    st.divider()

    # Multi-year deposit trend
    if not df_funnel_trend.empty:
        st.markdown("### Deposit Trend — All Years")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_funnel_trend["academic_year"], y=df_funnel_trend["deposited"],
            mode="lines+markers", name="Deposited",
            line=dict(color=MAROON, width=2.5), marker=dict(size=6)
        ))
        fig2.add_trace(go.Scatter(
            x=df_funnel_trend["academic_year"], y=df_funnel_trend["admitted"],
            mode="lines+markers", name="Admitted",
            line=dict(color=NAVY, width=2, dash="dot"), marker=dict(size=5)
        ))
        fig2.update_layout(
            height=300, margin=dict(t=20, b=20, l=20, r=20),
            legend=dict(orientation="h", y=-0.2),
            yaxis_title="Students"
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("mart_admissions_funnel · distribute/marts/admissions/mart_admissions_funnel")


# ══════════════════════════════════════════════════════════════════════════════
# REGISTRATION
# ══════════════════════════════════════════════════════════════════════════════
elif area == "Registration":
    logo_header("Registration")
    kpi_callout(
        "Section Fill Rate, Credits per FTE, Withdrawal Rate, "
        "Avg Section Size, Active Registration Holds, "
        "SAP Non-Compliance Rate, On-Track Students, Avg Cumulative GPA"
    )

    # Section utilization (latest year as integer, e.g. 2024)
    df_su = run_query(f"""
        SELECT
            academic_year,
            COUNT(*)                    AS total_sections,
            AVG(fill_rate)              AS avg_fill_rate,
            SUM(enrolled_count)         AS total_enrolled,
            AVG(enrolled_count)         AS avg_section_size,
            SUM(waitlisted_count)       AS total_waitlisted
        FROM {DB}.{SCHEMA}.MART_SECTION_UTILIZATION
        GROUP BY academic_year
        ORDER BY academic_year DESC
        LIMIT 1
    """)

    # Fill rate distribution by year
    df_su_trend = run_query(f"""
        SELECT academic_year, AVG(fill_rate) AS avg_fill_rate
        FROM {DB}.{SCHEMA}.MART_SECTION_UTILIZATION
        GROUP BY academic_year
        ORDER BY academic_year
    """)

    # Registration holds
    df_holds = run_query(f"""
        SELECT
            COUNT(DISTINCT student_id)                                         AS students_with_holds,
            COUNT(*)                                                            AS total_holds,
            SUM(CASE WHEN blocks_registration = TRUE THEN 1 ELSE 0 END)        AS blocking_holds
        FROM {DB}.{SCHEMA}.MART_REGISTRATION_HOLDS
        WHERE is_active = TRUE
    """)

    # Academic progress
    df_ap = run_query(f"""
        SELECT
            COUNT(DISTINCT student_id)                                             AS total_students,
            AVG(cumulative_gpa)                                                    AS avg_gpa,
            SUM(CASE WHEN is_sap_compliant = FALSE THEN 1 ELSE 0 END)             AS sap_non_compliant,
            SUM(CASE WHEN on_track_gpa_flag = TRUE
                      AND is_sap_compliant  = TRUE THEN 1 ELSE 0 END)             AS on_track
        FROM {DB}.{SCHEMA}.MART_ACADEMIC_PROGRESS
    """)

    # Enrollment census – withdrawal / credits / FTE (latest year)
    df_census_reg = run_query(f"""
        SELECT
            SUM(headcount)                  AS headcount,
            SUM(fte)                        AS fte,
            SUM(total_registered_hours)     AS total_credits,
            SUM(withdraw_count)             AS withdraw_count
        FROM {DB}.{SCHEMA}.MART_ENROLLMENT_CENSUS
        WHERE academic_year = (
            SELECT MAX(academic_year) FROM {DB}.{SCHEMA}.MART_ENROLLMENT_CENSUS
        )
    """)

    # ── KPI cards row 1: section metrics
    st.markdown("### Section Utilization")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if not df_su.empty and pd.notna(df_su.iloc[0]["avg_fill_rate"]):
            st.metric("Section Fill Rate", fmt_pct(df_su.iloc[0]["avg_fill_rate"]),
                      help="Avg enrolled / capacity across all sections")
        else:
            st.metric("Section Fill Rate", "—")
    with c2:
        if not df_su.empty and pd.notna(df_su.iloc[0]["avg_section_size"]):
            st.metric("Avg Section Size", fmt_num(df_su.iloc[0]["avg_section_size"], 1),
                      help="Average enrolled students per section")
        else:
            st.metric("Avg Section Size", "—")
    with c3:
        if not df_census_reg.empty and df_census_reg.iloc[0]["fte"] > 0:
            credits_per_fte = df_census_reg.iloc[0]["total_credits"] / df_census_reg.iloc[0]["fte"]
            st.metric("Credits per FTE", fmt_num(credits_per_fte, 1),
                      help="Total registered hours ÷ FTE")
        else:
            st.metric("Credits per FTE", "—")
    with c4:
        if not df_census_reg.empty and df_census_reg.iloc[0]["headcount"] > 0:
            wd_rate = df_census_reg.iloc[0]["withdraw_count"] / df_census_reg.iloc[0]["headcount"]
            st.metric("Withdrawal Rate", fmt_pct(wd_rate),
                      help="Withdrawals ÷ total headcount")
        else:
            st.metric("Withdrawal Rate", "—")

    # Section fill rate trend chart
    if not df_su_trend.empty:
        st.markdown("### Section Fill Rate Trend")
        fig = px.bar(
            df_su_trend, x="academic_year", y="avg_fill_rate",
            color_discrete_sequence=[MAROON],
            labels={"academic_year": "Academic Year", "avg_fill_rate": "Avg Fill Rate"}
        )
        fig.update_yaxes(tickformat=".0%")
        fig.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("mart_section_utilization · distribute/marts/registration/mart_section_utilization")

    st.divider()
    st.markdown("### Registration & Academic Health")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if not df_holds.empty and pd.notna(df_holds.iloc[0]["students_with_holds"]):
            st.metric("Students w/ Holds", fmt_num(df_holds.iloc[0]["students_with_holds"]),
                      help="Students with at least one active hold")
        else:
            st.metric("Students w/ Holds", "—")
    with c2:
        if not df_holds.empty and pd.notna(df_holds.iloc[0]["blocking_holds"]):
            st.metric("Blocking Holds", fmt_num(df_holds.iloc[0]["blocking_holds"]),
                      help="Holds that prevent registration")
        else:
            st.metric("Blocking Holds", "—")
    with c3:
        if not df_ap.empty and df_ap.iloc[0]["total_students"] > 0:
            sap_rate = df_ap.iloc[0]["sap_non_compliant"] / df_ap.iloc[0]["total_students"]
            st.metric("SAP Non-Compliance", fmt_pct(sap_rate),
                      help="Students failing satisfactory academic progress")
        else:
            st.metric("SAP Non-Compliance", "—")
    with c4:
        if not df_ap.empty and pd.notna(df_ap.iloc[0]["avg_gpa"]):
            st.metric("Avg Cumulative GPA", fmt_num(df_ap.iloc[0]["avg_gpa"], 2),
                      help="Average cumulative GPA across all active students")
        else:
            st.metric("Avg Cumulative GPA", "—")
    st.caption("mart_registration_holds · mart_academic_progress · distribute/marts/registration/")


# ══════════════════════════════════════════════════════════════════════════════
# FINANCIAL AID
# ══════════════════════════════════════════════════════════════════════════════
elif area == "Financial Aid":
    logo_header("Financial Aid")
    kpi_callout(
        "Avg Institutional Award, Aid Acceptance Rate, Packaging Completion Rate, "
        "Pell Recipient %, Loan Borrowing Rate, Verification Completion Rate, "
        "R2T4 Rate, SAP Compliance Rate, Aid Disbursement Trend"
    )

    # Latest year summary (aggregate across terms/programs)
    df_aid = run_query(f"""
        SELECT
            academic_year,
            SUM(enrolled_headcount)                                         AS enrolled_hc,
            SUM(aided_recipient_count)                                      AS aided_count,
            SUM(total_offered)                                              AS total_offered,
            SUM(total_accepted)                                             AS total_accepted,
            SUM(total_disbursed)                                            AS total_disbursed,
            AVG(avg_inst_award_per_recipient)                               AS avg_award,
            AVG(acceptance_rate)                                            AS avg_acceptance_rate,
            AVG(packaging_completion_rate)                                  AS avg_packaging_rate,
            AVG(pell_recipient_pct)                                         AS avg_pell_pct,
            AVG(loan_borrowing_rate)                                        AS avg_loan_rate,
            AVG(verification_completion_rate)                               AS avg_verification_rate,
            AVG(sap_compliance_rate)                                        AS avg_sap_rate
        FROM {DB}.{SCHEMA}.MART_AID_SUMMARY
        GROUP BY academic_year
        ORDER BY academic_year DESC
        LIMIT 1
    """)

    # Multi-year disbursement trend
    df_aid_trend = run_query(f"""
        SELECT
            academic_year,
            SUM(total_disbursed)           AS total_disbursed,
            SUM(aided_recipient_count)     AS aided_recipients
        FROM {DB}.{SCHEMA}.MART_AID_SUMMARY
        GROUP BY academic_year
        ORDER BY academic_year
    """)

    if not df_aid.empty:
        r = df_aid.iloc[0]
        st.markdown(f"### Financial Aid Snapshot — {r['academic_year']}")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Avg Inst. Award",      f"${float(r['avg_award']):,.0f}" if pd.notna(r['avg_award']) else "—",
                      help="Average institutional grant per aided recipient")
        with c2:
            st.metric("Aid Acceptance Rate",  fmt_pct(r["avg_acceptance_rate"]),
                      help="Accepted ÷ Offered")
        with c3:
            st.metric("Packaging Complete",   fmt_pct(r["avg_packaging_rate"]),
                      help="Students fully packaged ÷ total aided")
        with c4:
            st.metric("Pell Recipients",      fmt_pct(r["avg_pell_pct"]),
                      help="Students receiving Pell grants")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Loan Borrowing Rate",  fmt_pct(r["avg_loan_rate"]),
                      help="Students borrowing federal loans")
        with c2:
            st.metric("Verification Complete",fmt_pct(r["avg_verification_rate"]),
                      help="Verification selected students who completed")
        with c3:
            st.metric("SAP Compliance",       fmt_pct(r["avg_sap_rate"]),
                      help="Aid recipients meeting SAP standards")
        with c4:
            aided_pct = r["aided_count"] / r["enrolled_hc"] if pd.notna(r["enrolled_hc"]) and r["enrolled_hc"] > 0 else 0
            st.metric("Aid Participation",    fmt_pct(aided_pct),
                      help="% of enrolled students receiving institutional aid")

    # Disbursement trend
    if not df_aid_trend.empty:
        st.divider()
        st.markdown("### Aid Disbursement Trend")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_aid_trend["academic_year"],
            y=df_aid_trend["total_disbursed"],
            name="Total Disbursed",
            marker_color=MAROON
        ))
        fig.update_layout(
            height=320, margin=dict(t=20, b=20, l=20, r=20),
            yaxis_title="Total Disbursed ($)", yaxis_tickprefix="$", yaxis_tickformat=","
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("mart_aid_summary · distribute/marts/financial_aid/mart_aid_summary")

        # Recipient count trend
        st.markdown("### Aided Recipient Count Trend")
        fig2 = px.line(
            df_aid_trend, x="academic_year", y="aided_recipients",
            markers=True, color_discrete_sequence=[NAVY],
            labels={"academic_year": "Academic Year", "aided_recipients": "Aided Recipients"}
        )
        fig2.update_layout(height=280, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("mart_financial_aid_trend · distribute/marts/financial_aid/mart_financial_aid_trend")


# ══════════════════════════════════════════════════════════════════════════════
# ENROLLMENT MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
elif area == "Enrollment Management":
    logo_header("Enrollment Management")
    kpi_callout(
        "Total Headcount, FTE, Headcount by Level, Headcount Trend, "
        "Re-Enrollment Rate, YoY Rate Delta, "
        "1-Year Retention Rate, 4-Year Grad Rate, 6-Year Grad Rate, "
        "First-Gen Stop-Out Rate, URM Stop-Out Rate"
    )

    # Census headcount trend
    df_census = run_query(f"""
        SELECT
            academic_year,
            SUM(headcount) AS headcount,
            SUM(fte)       AS fte,
            SUM(CASE WHEN student_type = 'graduate' OR term_code LIKE '%GRAD%'
                     THEN headcount ELSE 0 END) AS grad_hc,
            SUM(CASE WHEN student_type != 'graduate' AND term_code NOT LIKE '%GRAD%'
                     THEN headcount ELSE 0 END) AS undg_hc
        FROM {DB}.{SCHEMA}.MART_ENROLLMENT_CENSUS
        GROUP BY academic_year
        ORDER BY academic_year
    """)

    # Latest year summary
    df_census_latest = run_query(f"""
        SELECT
            SUM(headcount)              AS headcount,
            SUM(fte)                    AS fte,
            SUM(withdraw_count)         AS withdrawals
        FROM {DB}.{SCHEMA}.MART_ENROLLMENT_CENSUS
        WHERE academic_year = (SELECT MAX(academic_year) FROM {DB}.{SCHEMA}.MART_ENROLLMENT_CENSUS)
    """)

    # Re-enrollment rate (latest)
    df_retention_snap = run_query(f"""
        SELECT
            degree_level,
            AVG(re_enrollment_rate)         AS re_enrollment_rate,
            AVG(prior_yr_re_enroll_rate)    AS prior_rate,
            AVG(rate_delta_yoy)             AS rate_delta
        FROM {DB}.{SCHEMA}.SNAP_RETENTION_TERM
        WHERE from_academic_year = (SELECT MAX(from_academic_year) FROM {DB}.{SCHEMA}.SNAP_RETENTION_TERM)
        GROUP BY degree_level
    """)

    # Cohort retention summary
    df_cohort = run_query(f"""
        SELECT
            AVG(yr1_retention_rate) AS avg_yr1,
            AVG(yr4_grad_rate)      AS avg_yr4,
            AVG(yr6_grad_rate)      AS avg_yr6,
            AVG(yr1_stop_out_rate)  AS avg_stop_out,
            AVG(first_gen_stop_out_rate) AS first_gen_stop_out,
            AVG(urm_stop_out_rate)  AS urm_stop_out
        FROM {DB}.{SCHEMA}.MART_RETENTION_COHORT_SUMMARY
        WHERE has_yr1_data = TRUE
    """)

    # ── KPI cards
    if not df_census_latest.empty:
        r = df_census_latest.iloc[0]
        st.markdown("### Current Enrollment")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Total Headcount", fmt_num(r["headcount"]), help="Current academic year headcount")
        with c2:
            st.metric("FTE",             fmt_num(r["fte"], 1),    help="Full-time equivalent enrollment")
        with c3:
            wd_rate = r["withdrawals"] / r["headcount"] if r["headcount"] > 0 else 0
            st.metric("Withdrawal Rate", fmt_pct(wd_rate), help="Withdrawals ÷ headcount")

    # Headcount trend
    if not df_census.empty:
        st.markdown("### Headcount Trend — All Years")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_census["academic_year"], y=df_census["undg_hc"],
            mode="lines+markers", name="Undergraduate",
            line=dict(color=GREEN, width=2.5), stackgroup="one"
        ))
        fig.add_trace(go.Scatter(
            x=df_census["academic_year"], y=df_census["grad_hc"],
            mode="lines+markers", name="Graduate",
            line=dict(color=BLUE, width=2.5), stackgroup="one"
        ))
        fig.update_layout(
            height=320, margin=dict(t=20, b=20, l=20, r=20),
            yaxis_title="Headcount",
            legend=dict(orientation="h", y=-0.2)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("mart_enrollment_census · distribute/marts/enrollment/mart_enrollment_census")

    st.divider()

    # Re-enrollment KPIs
    if not df_retention_snap.empty:
        st.markdown("### Re-Enrollment Rate (Retention Snapshot)")
        cols = st.columns(len(df_retention_snap))
        for i, row in df_retention_snap.iterrows():
            with cols[i % len(df_retention_snap)]:
                delta_pp = float(row["rate_delta"]) * 100 if pd.notna(row["rate_delta"]) else 0
                st.metric(
                    f"Re-Enrollment — {row['degree_level']}",
                    fmt_pct(row["re_enrollment_rate"]),
                    delta=f"{delta_pp:+.1f} pp vs prior yr",
                    help="Students registered next term ÷ eligible continuing"
                )
        st.caption("snap_retention_term · distribute/snapshots/snap_retention_term")

    st.divider()

    # Cohort graduation rates
    if not df_cohort.empty:
        r = df_cohort.iloc[0]
        st.markdown("### Cohort Outcome Rates")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("1-Year Retention",  fmt_pct(r["avg_yr1"]),    help="Avg across all programs with data")
        with c2:
            st.metric("4-Year Grad Rate",  fmt_pct(r["avg_yr4"]),    help="Avg 4-year graduation rate")
        with c3:
            st.metric("6-Year Grad Rate",  fmt_pct(r["avg_yr6"]),    help="Avg 6-year graduation rate")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Stop-Out Rate",       fmt_pct(r["avg_stop_out"]),    help="Overall year-1 stop-out")
        with c2:
            st.metric("First-Gen Stop-Out",  fmt_pct(r["first_gen_stop_out"]), help="First-generation student stop-out rate")
        with c3:
            st.metric("URM Stop-Out",        fmt_pct(r["urm_stop_out"]),    help="URM student stop-out rate")
        st.caption("mart_retention_cohort_summary · distribute/marts/enrollment/mart_retention_cohort_summary")


# ══════════════════════════════════════════════════════════════════════════════
# CROSS-DOMAIN
# ══════════════════════════════════════════════════════════════════════════════
elif area == "Cross-Domain":
    logo_header("Cross-Domain Analytics")
    kpi_callout(
        "Cohort Lifecycle Curve (enrolled / graduated / stopped-out), "
        "URM Rate Trend, Demographic Composition, "
        "First-Gen Rate, Full-Time Rate, "
        "Program Retention Comparison, Student At-Risk Count"
    )

    # Cohort lifecycle (milestone data)
    df_milestone = run_query(f"""
        SELECT
            years_since_entry,
            AVG(pct_still_enrolled) AS pct_enrolled,
            AVG(pct_graduated)      AS pct_graduated,
            AVG(pct_stopped_out)    AS pct_stopped_out
        FROM {DB}.{SCHEMA}.SNAP_COHORT_MILESTONE
        GROUP BY years_since_entry
        ORDER BY years_since_entry
    """)

    # Demographics trend (URM, first-gen, full-time)
    df_demo = run_query(f"""
        SELECT
            academic_year,
            SUM(total_headcount)    AS headcount,
            SUM(urm_count)          AS urm_count,
            SUM(first_gen_count)    AS first_gen_count,
            SUM(fulltime_count)     AS fulltime_count
        FROM {DB}.{SCHEMA}.MART_ENROLLMENT_DEMOGRAPHICS
        GROUP BY academic_year
        ORDER BY academic_year
    """)

    # At-risk students
    df_risk = run_query(f"""
        SELECT COUNT(DISTINCT student_id) AS at_risk_count
        FROM {DB}.{SCHEMA}.MART_STUDENT_AT_RISK
        WHERE is_at_risk = TRUE
    """)

    # Program retention comparison
    df_prog_ret = run_query(f"""
        SELECT
            program_name,
            AVG(yr1_retention_rate) AS yr1_rate,
            AVG(yr6_grad_rate)      AS yr6_rate,
            AVG(cohort_size)        AS avg_cohort_size
        FROM {DB}.{SCHEMA}.MART_RETENTION_COHORT_SUMMARY
        WHERE has_yr1_data = TRUE
        GROUP BY program_name
        ORDER BY yr1_rate DESC
        LIMIT 10
    """)

    # ── Cohort lifecycle stacked area
    if not df_milestone.empty:
        st.markdown("### Cohort Lifecycle Curve")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_milestone["years_since_entry"], y=df_milestone["pct_enrolled"],
            name="Still Enrolled", mode="lines",
            line=dict(color=BLUE), fill="tozeroy", fillcolor="rgba(66,133,244,0.15)"
        ))
        fig.add_trace(go.Scatter(
            x=df_milestone["years_since_entry"], y=df_milestone["pct_graduated"],
            name="Graduated", mode="lines",
            line=dict(color=GREEN), fill="tozeroy", fillcolor="rgba(92,134,29,0.15)"
        ))
        fig.add_trace(go.Scatter(
            x=df_milestone["years_since_entry"], y=df_milestone["pct_stopped_out"],
            name="Stopped Out", mode="lines",
            line=dict(color=RED), fill="tozeroy", fillcolor="rgba(184,57,43,0.10)"
        ))
        fig.update_layout(
            height=340, margin=dict(t=20, b=20, l=20, r=20),
            xaxis_title="Years Since Entry",
            yaxis_title="% of Cohort", yaxis_tickformat=".0%",
            legend=dict(orientation="h", y=-0.25)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("snap_cohort_milestone · distribute/snapshots/snap_cohort_milestone")

    st.divider()

    # Demographics KPIs + trend
    if not df_demo.empty and not df_demo.empty:
        latest = df_demo.iloc[-1]
        hc = latest["headcount"]
        urm_rate     = latest["urm_count"]     / hc if hc > 0 else 0
        fg_rate      = latest["first_gen_count"] / hc if hc > 0 else 0
        ft_rate      = latest["fulltime_count"]  / hc if hc > 0 else 0

        st.markdown("### Demographic Profile — Latest Year")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            at_risk = int(df_risk.iloc[0]["at_risk_count"]) if not df_risk.empty and pd.notna(df_risk.iloc[0]["at_risk_count"]) else 0
            st.metric("Students At-Risk",  fmt_num(at_risk),       help="Students flagged for early alert intervention")
        with c2:
            st.metric("URM Rate",         fmt_pct(urm_rate),        help="Underrepresented minority students")
        with c3:
            st.metric("First-Gen Rate",   fmt_pct(fg_rate),         help="First-generation college students")
        with c4:
            st.metric("Full-Time Rate",   fmt_pct(ft_rate),         help="Students enrolled full-time")

        # URM trend
        df_demo["urm_rate"] = df_demo["urm_count"] / df_demo["headcount"]
        df_demo["fg_rate"]  = df_demo["first_gen_count"] / df_demo["headcount"]

        st.markdown("### URM & First-Gen Rate Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_demo["academic_year"], y=df_demo["urm_rate"],
            name="URM Rate", mode="lines+markers",
            line=dict(color=MAROON, width=2.5), marker=dict(size=6)
        ))
        fig.add_trace(go.Scatter(
            x=df_demo["academic_year"], y=df_demo["fg_rate"],
            name="First-Gen Rate", mode="lines+markers",
            line=dict(color=NAVY, width=2, dash="dot"), marker=dict(size=5)
        ))
        fig.update_layout(
            height=300, margin=dict(t=20, b=20, l=20, r=20),
            yaxis_tickformat=".0%", yaxis_title="Rate",
            legend=dict(orientation="h", y=-0.25)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("mart_enrollment_demographics · distribute/marts/enrollment/mart_enrollment_demographics")

    st.divider()

    # Program retention comparison
    if not df_prog_ret.empty:
        st.markdown("### 1-Year Retention by Program")
        fig = px.bar(
            df_prog_ret, x="yr1_rate", y="program_name", orientation="h",
            color="yr1_rate", color_continuous_scale=[[0, RED], [0.5, AMBER], [1.0, GREEN]],
            labels={"yr1_rate": "1-Yr Retention Rate", "program_name": "Program"},
            text=df_prog_ret["yr1_rate"].apply(lambda v: fmt_pct(v))
        )
        fig.update_xaxes(tickformat=".0%")
        fig.update_traces(textposition="outside")
        fig.update_layout(
            height=420, margin=dict(t=20, b=20, l=20, r=20),
            coloraxis_showscale=False, yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("mart_retention_cohort_summary · distribute/marts/enrollment/mart_retention_cohort_summary")


# ══════════════════════════════════════════════════════════════════════════════
# BENCHMARKING
# ══════════════════════════════════════════════════════════════════════════════
elif area == "Benchmarking":
    logo_header("Benchmarking")

    st.markdown("""
    <div class="kpi-callout">
        <strong>College Scorecard Benchmarks</strong> — Program-level outcomes from the U.S. Department of Education.
        Includes earnings, debt, default rates, and repayment metrics by CIP code and credential level.
    </div>
    """, unsafe_allow_html=True)

    # Program earnings vs debt ROI
    df_scorecard = run_query(f"""
        SELECT
            cip_desc,
            credential_level_desc,
            earn_median_4yr,
            debt_median_all,
            earnings_to_debt_ratio_4yr AS earn_to_debt_ratio,
            earn_vs_national_pct
        FROM {DB}.{SCHEMA}.MART_SCORECARD_PROGRAM_OUTCOMES
        WHERE is_own_institution = TRUE
          AND is_suppressed = FALSE
          AND earn_median_4yr IS NOT NULL
          AND earnings_to_debt_ratio_4yr IS NOT NULL
        ORDER BY earnings_to_debt_ratio_4yr DESC NULLS LAST
        LIMIT 10
    """)

    if not df_scorecard.empty:
        st.markdown("### Program Earnings vs. Debt ROI")
        st.markdown("Top 10 programs by earnings-to-debt ratio")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_scorecard["cip_desc"],
            y=df_scorecard["earn_to_debt_ratio"],
            marker=dict(color=BLUE),
            text=df_scorecard["earn_to_debt_ratio"].apply(lambda x: f"{x:.2f}x" if pd.notna(x) else ""),
            textposition="outside",
            name="Earn-to-Debt Ratio"
        ))
        fig.update_layout(
            height=400,
            xaxis_title="Program",
            yaxis_title="Earnings / Debt Ratio",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Earnings vs. National Benchmarks")
        c1, c2, c3 = st.columns(3)
        above_nat = (df_scorecard["earn_vs_national_pct"] > 0).sum()
        below_nat = (df_scorecard["earn_vs_national_pct"] < 0).sum()
        with c1:
            st.metric("Programs Above National Median", above_nat)
        with c2:
            st.metric("Programs Below National Median", below_nat)
        with c3:
            avg_vs_nat = df_scorecard["earn_vs_national_pct"].mean()
            st.metric("Avg vs National", fmt_pct(avg_vs_nat, decimals=1))

    # Pell vs Non-Pell earnings gap
    df_pell_gap = run_query(f"""
        SELECT
            cip_desc,
            earn_median_pell_4yr,
            earn_median_nopell_4yr,
            earn_median_nopell_4yr - earn_median_pell_4yr AS earnings_gap
        FROM {DB}.{SCHEMA}.MART_SCORECARD_PROGRAM_OUTCOMES
        WHERE is_own_institution = TRUE
          AND is_suppressed = FALSE
          AND earn_median_pell_4yr IS NOT NULL
          AND earn_median_nopell_4yr IS NOT NULL
        ORDER BY earnings_gap DESC
        LIMIT 10
    """)

    if not df_pell_gap.empty:
        st.markdown("### Pell vs. Non-Pell Earnings Gap")
        st.markdown("Programs with largest earnings gaps (equity concern)")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_pell_gap["cip_desc"],
            y=df_pell_gap["earnings_gap"],
            marker=dict(color=MAROON),
            text=df_pell_gap["earnings_gap"].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else ""),
            textposition="outside",
            name="Earnings Gap"
        ))
        fig.update_layout(
            height=400,
            xaxis_title="Program",
            yaxis_title="Non-Pell Earnings - Pell Earnings ($)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    st.caption("mart_scorecard_program_outcomes · distribute/marts/summaries/enrollment/mart_scorecard_program_outcomes")
