function varargout = test_318(varargin)
% TEST_318 MATLAB code for test_318.fig
%      TEST_318, by itself, creates a new TEST_318 or raises the existing
%      singleton*.
%
%      H = TEST_318 returns the handle to a new TEST_318 or the handle to
%      the existing singleton*.
%
%      TEST_318('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in TEST_318.M with the given input arguments.
%
%      TEST_318('Property','Value',...) creates a new TEST_318 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before test_318_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to test_318_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above output1 to modify the response to help test_318

% Last Modified by GUIDE v2.5 18-Mar-2016 12:36:44

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @test_318_OpeningFcn, ...
    'gui_OutputFcn',  @test_318_OutputFcn, ...
    'gui_LayoutFcn',  [] , ...
    'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before test_318 is made visible.
function test_318_OpeningFcn(hObject, ~, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to test_318 (see VARARGIN)

% Choose default command line output for test_318
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes test_318 wait for user response (see UIREtimesOfHeadE)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = test_318_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in plot.
function plot_Callback(hObject, eventdata, handles)
% hObject    handle to plot (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
hold off;      % clear the plot
%==============================================================%
counter = zeros(101,1);         % count the number of head times of each 100 flips for 10,000 times
for times = 1:10000
    random = rand(100,1);   % generate 100 random numbers from 0 to 1
    a = zeros(100,1);          % generate 100 zeros to save the head times of 100 filps
    p1 = str2double(get(handles.p1, 'string'));     % get the input number, change the type to double
    a(random < p1) = 1;       % set the probability
    timesOfHead = sum(a);
    % timeOfHead maps to counter(timeOfHead+1
    counter(timesOfHead+1) = counter(timesOfHead+1) + 1;
    x = 0:1:100;    % set x axes from 1 to 100
end
%   === plot the figure === %
y1 = counter(x+1);
plot(handles.axes1, x, y1, 'r--');
hold on
%==============================================================%
% === calculate the E(X), D(X)  of P1===%
EX = 0;
EX2 = 0;
for times = 0:100
    EX = x(times+1) * y1(times+1)/10000 + EX;
    EX2 = x(times+1) * x(times+1) * y1(times+1) / 10000 + EX2;
end
set(handles.output1, 'string', {['E(X)=' num2str(EX)]; ['Var(X)=' num2str(EX2 - EX^2)]});
%==============================================================%
% ====  nearly the same as above ===%
counter = zeros(101,1);
for times = 1:10000
    random = rand(100,1);
    a = zeros(100,1);
    p2 = str2double(get(handles.p2, 'string')); % maybe p2 rather than p1 is the only difference
    a (random < p2) = 1;
    timesOfHead = sum(a);
    counter(timesOfHead + 1) = counter( timesOfHead+1) + 1;
    x = 0:1:100;
end
%   === ploy the figure ===%
y2 = counter(x+1);
plot(handles.axes1, x, y2, 'b--');
xlabel('head times of 100 flips');
ylabel('total head times of every 100 flips');
legend('p1','p2');
%==============================================================%
% === calculate the E(X) and D(X) ===%
EY = 0;
EY2 = 0;
for times = 0:100
    EY = x(times+1) * y2(times+1)/10000 + EY;
    EY2 = x(times+1) * x(times+1) * y2(times+1) / 10000 + EY2;
end
set(handles.output2,'string', {['E(Y)=' num2str(EY)]; ['Var(Y)=' num2str(EY2 - EY^2)]});
%==============================================================%
%  === find intersection and calculate the accuracy  ===%
ex = 0;
middle = 0;
for index = 1:1:100
    if(p1>p2&&y1(index)>=y2(index)&&y2(index)~=0)   % first case
        middle = index;
        for  x= middle:1:100    % from middle to 100
            ex = ex + x * y1(x+1)/10000;    % compute ex, just like EX
        end
        set(handles.output3, 'string',  {num2str(middle); num2str(ex/EX)}); % show output and break
        break;
    elseif(p1<p2&&y2(index)>=y1(index)&&y2(index)~=0)   % another case
        middle = index;
        for x = 0:1:middle-2    % from 0 to middle-2
            ex = ex + x*y1(x+1)/10000;  % compute ex, just like EX
        end
        set(handles.output3, 'string',  {num2str(middle); num2str(ex/EX)}); % show output and break
        break;
    else % if p1 and p2 are too close, we set middle to 0, so the accuracy will be set to 1
        middle = 0;
    end
end
if(middle ==0)
    set(handles.output3, 'string' , {'None', num2str(1.00)});   % middle = 0 and accuracy set to 1
end

function p1_Callback(hObject, eventdata, handles)
% hObject    handle to p1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of p1 as output1
%        str2double(get(hObject,'String')) returns contents of p1 as a double


% --- Executes during object creation, after setting all properties.
function p1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to p1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function p2_Callback(hObject, eventdata, handles)
% hObject    handle to p2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of p2 as output1
%        str2double(get(hObject,'String')) returns contents of p2 as a double


% --- Executes during object creation, after setting all properties.
function p2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to p2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
