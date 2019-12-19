# Alpha Notes

### [Alpha Heuristic for Leverage / Scaling (Quantopian)](https://www.quantopian.com/posts/enhancing-short-term-mean-reversion-strategies-1)

#### Guy Fleury Mar 17, 2017

> @Anthony, you start with the usual: A(t) = A(0)∙(1 + r)^t where r is viewed as the average market return which you can have just by buying SPY, DIA, or QQQ, and holding on for the duration.
>
> You want to design a trading strategy that is scalable: A(t) = k∙A(0)∙(1 + r)^t. Note that buying k SPY and holding is scalable 100%. It is also why I design my trading strategies to be scalable. Otherwise, how could they ever reach the level of managing a large portfolio if they were not scalable.
>
> You want to trade, then you have to outperform the average. Bring some alpha to the mix. This will result in: A(t) = k∙A(0)∙(1 + r + α)^t where α represent the premium or contribution your trading skills bring to the problem.
>
> Evidently, your skills needs to have a positive impact (α > 0). Nonetheless, you still want the strategy to be scalable. As previously observed, this particular trading strategy is not that scalable down. If you go small, it will simply destroy the account. It is only partially scalable up. But, still, it can generate some alpha. And, positive alpha translate to outperforming averages, generating more money which was the whole purpose of the game.
>
> IB charges less than 3% for leverage, but leverage is only for the sum exceeding your equity. It is only when leverage exceeds one; L > 1.00 that you will be charged interests on the excess. So you can get an approximation using: A(t) = k∙A(0)∙(1 + r + α – 0.03)^t. Using leverage is the same as increasing the bet size and therefore it will have an impact on the overall score, giving: A(t) = (1 + L)∙k∙A(0)∙(1 + r + α - 0.03)^t.
>
> The strategy was not using 100% leverage, but 60%. It was designed as a 130/30 hedge fund after all. This would have for impact to reduce the leveraging estimate to:
> A(t) = (1 + L)∙k∙A(0)∙(1 + r + α – 0.03\*0.60)^t.
>
> With the modifications to Blue's program (two numbers) I got: r + α = 21.87%, L = 0.60, A(0) = \$1M, and t = 14.36 years.
>
> My simulation did put k = 5 since I wanted to see the extent of the strategy's scalability. On that front, the trading strategy did not respond that well. It is understandable, it does not make any compensation for return degradation over time. But, that is a flaw that can be corrected, and doing so will improve performance even more.

#### Guy Fleury Mar 18, 2017

> @Anthony, the formula used is very basic. It considers the end points, not the path to get there. Nonetheless, the end points give the same numbers, an as if.
>
> A(t) represents the ongoing net liquidating value of a portfolio (sum of its assets). You could also express the same thing using:
> A(t) = A(0) + Ʃ ƒ H(t)∙dP which reads the same. A(t) is the sum of the initial capital to which is added the end results of all trades.
>
> A(0) is the initial portfolio value (usually the available initial trading capital).
>
> r is the compounded annual growth rate (CAGR). Here, r is expressed as the average market return. It can also serve as the most expected portfolio outcome for someone playing for the long term, say more than 10 years.
>
> t is for the time in years. In this case t was for 14.36 years.
>
> k is just a scaling factor. You put 2 times more in initial capital (2∙A(0)), you should expect 2 times more in total profits. This, if the strategy is scalable.
>
> The alpha α is used in the same way as Jensen presented it in the late 60's. It is for the skills brought to the game. A positive alpha meant that what you did in managing a portfolio was beneficial since it was adding to the CAGR.
>
> What Jensen observed in his seminal paper was that the average portfolio manager had a negative alpha. Meaning that what they did, on average, was detrimental to their overall long term performance since the majority of them ended up not beating the averages. Your trading script needs to generate a positive alpha (α > 0), otherwise your portfolio might fall in the above cited category.
>
> L is for the leverage. There are no leveraging fees for L < 1.00 since it is equivalent to be not fully invested. In Blue's program, if you wanted a leverage of 2.00, you could change one, or two numbers to do the job. As was said, leveraging has the same impact as increasing the bet size. You pay for the ability of doing so.
>
> What you want your program to do is have your α > lc, its leveraging charge (lc). I don't find leveraging a trading strategy interesting unless it has an α > 2∙lc, meaning the added alpha is at least twice the leveraging charges. Otherwise you might be trading for the benefit of the broker, not your own. And as you know, the result could be even worse if the trading strategy is not well behaved or well controlled.
>
> So, with the presented equation, one can estimate the outcome of different scenarios even before performing them knowing what will be the impact on total return. If you set k = 5, meaning 5 times more initial capital, you should expect 5 times more profits. If you don't get it, then your program is showing weaknesses in the scalability department. This should lead to finding ways to compensate for the performance degradation.

#### Guy Fleury Mar 25, 2017

> @Grant, I think we simply have a different viewpoint.
>
> For me, an automated trading strategy needs to be upward scalable. If not, its value is considerably reduced.
>
> If scaling up for whatever trading methods used gets to produce over the long haul less than market average, then a strategy becomes literally worthless since the alternative of buying an index fund would have generated more for a lot less work.
>
> No one will put 1,000 $10k strategies to work ($10M). Especially if you have 10 times or 100 times more capital to invest. You need scalable strategies that will not break down under AUM pressure. You also need machines that can handle the data and execute the trades. You need not only a doable, but also a feasible scenario that can handle A(t) for the entire trading/investing interval. This trading interval can not be just for a few years, otherwise you are just taking a timing bet where the period you activate your account becomes the most important.
>
> Also, as you must have seen numerous times here, having a $10k strategy is by no means a guaranteed viable scenario at $100k, $1M, or $10M for that matter. The problems encountered at each level are quite different, and this just based on the initial capital put to work.
>
> I've given this formula elsewhere: `A(t) = (1+L)∙k∙A(0)∙(1 + r + α - lc% - fc%)^t`, and what I see as dreamland is expecting some positive alpha for a 50/50 long short portfolio with a near zero beta. The examples that have been presented on Q failed that acid test: `α > 0`. And it usually gets worse when you scale them up: k∙A(0), increase the trading interval, account for frictional costs fc%, and leveraging fees lc%.
>
> There are 3 ways to improve the Sharpe ratio. One is to really increase your portfolio average return (generate some alpha). Another is to reduce volatility. And the other is to do both at the same time. However, anytime you want to reduce volatility, it entails on average, lower risks but also lower returns.
>
> So, for someone wishing some Q allocation or even just a viable trading strategy, they should understand the implications of the formula: `A(t) = (1+v∙L)∙k∙A(0)∙(1 + r + α – v∙lc% – v∙fc%)^t` where r, the market average, will be reduced by a negative alpha α. And where leveraging fees and frictional costs will be v times the leveraging boost. Evidently, if v = 1 (no boost), k = 1 (no scaling), lc% = 0 (no leverage), you are left with: `A(t) = A(0)∙(1 + r + α – fc%)^t` since commissions will still have to be paid. Then, you better have some trading skills to outperform the average (α > fc%).
>
> I don't see that as a very pretty picture. The only remedy is to have a positive alpha of sufficient size to compensate for all the drawbacks. Even the one rarely discussed here which is long term return degradation.
>
> I am from the outside, and I would never put anybody's strategy to work without testing the above formula on a sufficiently large portfolio over an extended period of time which is what I do using Q, explore their limits, see how far they can go, where will they break down?
>
> It is like if you can not show me that your trading strategy is scalable upwards, what is its value? If you can show that it can generate some alpha, again what could be its value going forward? And if it is not leverageable, how can we push it further to do even more?
>
> For me, it does not matter which trading methods you use, my interest is only on A(t). And the score for A(t) is kept on the bottom line of the trading account.
>
> However you want to look at it. If you want more, you will have to do more than the other guy.
>
> It's like if we have the exact same car and take a long race to the finish line. Our respective driving skills will matter. But regardless, I could get a definite positive edge just by changing the tires. Then driving skills might not matter much
