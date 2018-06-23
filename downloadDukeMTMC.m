dataset = [];
dataset.numCameras = 8;
dataset.videoParts = [9, 9, 9, 9, 9, 8, 8, 9];

% Set this accordingly
dataset.savePath = './'; 
ffmpegPath = '/usr/local/bin/'; % Used to extract frames from videos

options = weboptions('Timeout', 60);

%%
fprintf('Patience, this may take 1-2 days!\n');

% Create folder structure
fprintf('Creating folder structure...\n');
mkdir(dataset.savePath);
folders = {'ground_truth','calibration','detections','frames','masks','videos'};
for k = 1:length(folders)
    mkdir([dataset.savePath, folders{k}]);
end

for k = 1:dataset.numCameras
    mkdir([dataset.savePath 'frames/camera' num2str(k)]);
    mkdir([dataset.savePath 'masks/camera' num2str(k)]);
    mkdir([dataset.savePath 'videos/camera' num2str(k)]);
end

% Download ground truth
fprintf('Downloading ground truth...\n');
filenames = {'trainval.mat', 'trainvalRaw.mat'};
urls = {'http://vision.cs.duke.edu/DukeMTMC/data/ground_truth/trainval.mat', ...
        'http://vision.cs.duke.edu/DukeMTMC/data/ground_truth/trainvalRaw.mat'};
for k = 1:length(urls)
    filename = sprintf('%sground_truth/%s',dataset.savePath,filenames{k});
    fprintf([filename '\n']);
    websave(filename,urls{k},options);
end

% Download calibration
fprintf('Downloading calibration...\n');
urls = {'http://vision.cs.duke.edu/DukeMTMC/data/calibration/calibration.txt', ...
        'http://vision.cs.duke.edu/DukeMTMC/data/calibration/camera_position.txt', ...
        'http://vision.cs.duke.edu/DukeMTMC/data/calibration/ROIs.txt'};
filenames = {'calibration.txt', 'camera_position.txt', 'ROIs.txt'};

for k = 1:length(urls)
    filename = sprintf('%scalibration/%s',dataset.savePath,filenames{k});
    fprintf([filename '\n']);
    websave(filename,urls{k},options);
end

% Download detections
fprintf('Downloading detections...\n');
for cam = 1:dataset.numCameras
    url = sprintf('http://vision.cs.duke.edu/DukeMTMC/data/detections/camera%d.mat',cam);
    filename = sprintf('%sdetections/camera%d.mat',dataset.savePath,cam);
    fprintf([filename '\n']);
    websave(filename,url,options);
end

% Download masks
fprintf('Downloading masks...\n');
for cam = 1:dataset.numCameras
    url = sprintf('http://vision.cs.duke.edu/DukeMTMC/data/masks/camera%d.tar.gz',cam);
    filename = sprintf('%smasks/camera%d.tar.gz',dataset.savePath,cam);
    fprintf([filename '\n']);
    websave(filename,url,options);
end

% Download videos
fprintf('Downloading videos...\n');
for cam = 1:dataset.numCameras
    for part = 0:dataset.videoParts(cam)
        url = sprintf('http://vision.cs.duke.edu/DukeMTMC/data/videos/camera%d/%05d.MTS',cam,part);
        filename = sprintf('%svideos/camera%d/%05d.MTS',dataset.savePath,cam,part);
        fprintf([filename '\n']);
        websave(filename,url,options);
    end
end
fprintf('Data download complete.\n');

% Extract masks
fprintf('Extracting masks...\n');
for cam = 1:dataset.numCameras
    filename = sprintf('%smasks/camera%d.tar.gz',dataset.savePath,cam);
    fprintf([filename '\n']);
    untar(filename, [dataset.savePath 'masks']);
end

% Delete temporary files
fprintf('Deleting temporary files...\n');
for cam = 1:dataset.numCameras
    filename = sprintf('%smasks/camera%d.tar.gz',dataset.savePath,cam);
    fprintf([filename '\n']);
    delete(filename);
end

% Extract frames
fprintf('Extracting frames...\n');
currDir = pwd;
for cam = 1:dataset.numCameras
    cd([dataset.savePath 'videos/camera' num2str(cam)]); 
    filelist = '"concat:00000.MTS';
    for k = 1:dataset.videoParts(cam), filelist = [filelist, '|0000', num2str(k), '.MTS']; end; 
    framesDir = [dataset.savePath 'frames/camera' num2str(cam) '/%d.jpg'];
    command = [ffmpegPath ' -i ' filelist '" -qscale:v 1 -f image2 ' framesDir];
    system(command);
end
cd(currDir);
fprintf('All done!\n');
fprintf('If extraction failed, make sure you have sufficient disk space.\n');





