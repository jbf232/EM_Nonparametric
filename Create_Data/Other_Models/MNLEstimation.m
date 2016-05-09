
        
offer = dlmread('Other_Models/SalesData.txt', '%d');
purchase = dlmread('Other_Models/Purchases.txt', '%d');

D=size(offer);
numProds=D(2);
T=D(1)


percent=0.99;
trainCutOff=floor(percent*(T));
S=offer(1:trainCutOff,:);
Z=purchase(1:trainCutOff,:);
SVal=offer((trainCutOff)+1:T,:);
ZVal=purchase((trainCutOff)+1:T,:);
testLength = T- trainCutOff;

v_hat = zeros(1,numProds);

options=optimset('MaxFunEvals',10000,'Display','off');
%Create and maximize log likelihood for MNL
minus_log_L = @(v) -( sum(sum(Z.*repmat([0 v(2:numProds)], trainCutOff,1),2))  - (sum(log(sum(exp(repmat([0 v(2:numProds)], trainCutOff,1)).*S,2)))) );
minus_log_LVal = @(v) -( sum(sum(ZVal.*repmat([0 v(2:numProds)],testLength,1),2))  - (sum(log(sum(exp(repmat([0 v(2:numProds)],testLength,1)).*SVal,2)))) );
[v,fvalMNL] = fmincon(minus_log_L,v_hat,[],[],[],[],[],[],[],options);
prefWeights= exp(v);

-minus_log_LVal(v)
