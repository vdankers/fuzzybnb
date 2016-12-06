%% Read
% Read features from csv file, make sure that column names are removed
features = csvread('train_features.csv');
% csvwrite('train_features.dat',a)

% Initalize empty array for the predicted values
predicted_y = ones(2753,1);

%% Read settings for FIS
fismat = readfis('airbnb.fis');

%% Predict for test data
for n = 1:2753
  output = evalfis(features(n,:),fismat);
  predicted_y(n,1) = output;
end

%% Save predicted values as CSV file

csvwrite('predicted_prices.csv',predicted_y)