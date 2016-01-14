%Coryn Scott

imgUrls = textread('localurl.txt', '%s');
numImg = length(imgUrls);

% Parameters:
clear param
param.imageSize = [256 256]; % it works also with non-square images
param.orientationsPerScale = [8 8 8 8];
param.numberBlocks = 4;
param.fc_prefilt = 4;

% Computing gist requires 1) prefilter image, 2) filter image and collect
% output energies



for i=1:numImg
    img = imread(imgUrls{i});
    [gist, param] = LMgist(img, '', param);
    gistVals(i,:) = gist;
    
end