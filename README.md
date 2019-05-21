#### Description

This is an api to get personality scores for arbitrary twitter users. By default, for any request made, scores for [@austen](twitter.com/austen) will be returned, as a means of demonstrating
its output. To get the scores for a particular user submit a POST request with JSON like so: `{ "username": "elonmusk" }`. This will return personality scores for the [Elon Musk's twitter
account](twitter.com/elonmusk).

Endpoint: [https://mif88l63ba.execute-api.us-west-2.amazonaws.com/default/personality-score](https://mif88l63ba.execute-api.us-west-2.amazonaws.com/default/personality-score)

#### Examples

To get test data from [@austen](twitter.com/austen):
```
curl https://mif88l63ba.execute-api.us-west-2.amazonaws.com/default/personality-score
```

To get data from [@elonmusk](twitter.com/elonmusk): 
```
curl -X POST --data '{ "username": "elonmusk" }' https://mif88l63ba.execute-api.us-west-2.amazonaws.com/default/personality-score
```
