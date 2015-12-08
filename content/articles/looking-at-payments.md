Title: Looking at payments solution for SAAS in Europe
Date: 2015-12-08
Short_summary: Payments in Europe are complicated due to VAT, I look at what a SAAS could use
Category: Product
Authors: Vincent


As we are working on our product (if you work in an agency, we'd love to have a chat with you! send us a mail at team AT wearewizards.io), I was curious to see the payments landscape in Europe, having read so much about [#VATMESS](https://twitter.com/hashtag/vatmess).
<!-- PELICAN_END_SUMMARY -->

Most Software As A Service business operate with monthly plans with various tiers. 
In Europe, before 2015, the supplier would charge their own VAT rate to their customers: for example if the supplier was based in the UK and the customer in France, the supplier would charge the UK VAT rate.

since 2015 however, the supplier now has to charge the VAT rate where the customer is located and report sales to that country. This change was made to prevent unfair competitions from countries with a lower VAT rate, with big companies moving to Luxembourg for example. Regulators only forgot to set a lower limit (they are apparently now thinking of a £5k limit) and didn't think of SME or thought about it and decided that crippling european businesses would be a good idea.
Note that this change only applies to B2C customers.

This article will focus on what it means for a UK based VAT registered company as it is our case.


# Business side
The UK has put in place something called the VAT Mini One Stop Shop or VAT MOSS (https://www.gov.uk/guidance/register-and-use-the-vat-mini-one-stop-shop). This allows businesses to register in only one country and let it redistribute the money after filing a VAT return for other countries on a quarterly basis.

If the customer is a business and is VAT registered, just getting the VAT number and checking it should be enough. However, companies paying without giving their VAT number or non-VAT registered ones should be treated as B2C.

As mentioned in the introduction, we need to charge the VAT of the customer which means we need to locate it.

Here are some examples of pieces of informations we can use:

- billing address
- ip address geolocation
- bank location
- card location

Note that the legislation requires to have 2 non-conflicting informations and keep that for 10 (!) years. 
If you don't manage that, you are supposed to reject the transaction. You could possibly ask for the user to send some proof by mail but that's a terrible user experience.

If we manage to get customers to pay us, we then need to separate sales by country and apply the right VAT. This gives us the amount of tax we need to pay for each country.

# Coding
Now that we have an overview of what the VAT system looks like, let's have a look at the solutions.

## Payment providers
None of these actually help with the VAT mess but are still needed.
There are a few alternatives here:

- [Stripe](https://stripe.com)
- [Braintree](https://www.braintreepayments.com/)
- [Paymill](https://www.paymill.com/)

Paymill is based in Europe. Stripe is extremely easy to setup and get started. I haven't used the other two so I can't comment on those but it seems you need to be approved for a merchant account for them which means some some wait.

Here are the advertised rates (you can possibly get a better one by talking with them):
- Paymill: 2.95% + 0.28€
- Braintree: 2.4% + 20p (first £30k free) for EU cards, 3.4% + 20p for non EU cards
- Stripe: 1.9% + 20p for UK cards and 2.9% + 20p for foreign cards

Let's use a small example to see the difference: £10k sales with £5k from the UK, £3k from NA and £2k from Europe with let's say 100 transactions

```python
paymill = (2.95 * 10000 / 100) - (0.20 * 100)
>> 275
braintree = (2.4 * 7000 / 100) + (3.4 * 3000 / 100) - (0.20 * 100)
>> 250
stripe = (1.9 * 5000 / 100) + (2.9 * 5000 / 100) - (0.20 * 100)
>> 220
```

Stripe seems to give the best price but keep in mind you cand probably get better rates than the advertised one (at least for Paymill according to the employee I met ages ago).

## Handling VAT

### Implementing it yourself
You need to handle a few cases:

#### Customer is VAT registered
Ask for VAT number and use your country VAT is customer is based in your country or no VAT otherwise

#### Customer doesn't provide VAT number
Ask for country (that can be prefilled based on IP address) and compare with the IP location. If it matches continue otherwise compare the country filled with the bank country. If it matches continue otherwise ask the customer to send a fax with their certificate of birth and a passport. More seriously what should be done in the last case? 

There are APIs to get up-to-date VAT rates and check VAT numbers but you could use [pyvat](https://github.com/iconfinder/pyvat) for example to handle all of that for you.

While this is annoying, it doesn't seem like a huge amount of work.


### Using a third party
If you prefer using off-the-shelf solutions, a few exist that handle the VAT aspect (note that I haven't used any of them):


- [Recurly](https://recurly.com/): $99/month and 10¢ per transaction + 1.25% of revenue (on top of payment gateway)
- [Quaderno](https://quaderno.io/): $29/month on top of your payment provider, provides a widget for checkout that handles European VAT rules
- [Taxamo](https://www.taxamo.com): £40/months for all the regions, pretty limited number of country as it's missing Canada and Australia for example. Doesn't actually show what the product is but included for completeness

Out of those, Quaderno seems to be the best choice and is fairly cheap.


## Conclusion
As a developer I would be tempted to write my own version but Quaderno seems like a good fit and is cheap enough for a B2B SAAS that it might be worth avoiding the hassle of coding it.

Looking for feedback really, quite curious of how people are doing on that side and if anything has experience with Quaderno and the others.
