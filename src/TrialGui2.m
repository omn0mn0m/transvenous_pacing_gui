function varargout = TrialGui2(varargin)
% TRIALGUI2 MATLAB code for TrialGui2.fig
%      TRIALGUI2, by itself, creates a new TRIALGUI2 or raises the existing
%      singleton*.
%
%      H = TRIALGUI2 returns the handle to a new TRIALGUI2 or the handle to
%      the existing singleton*.
%
%      TRIALGUI2('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in TRIALGUI2.M with the given input arguments.
%
%      TRIALGUI2('Property','Value',...) creates a new TRIALGUI2 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before TrialGui2_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to TrialGui2_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help TrialGui2

% Last Modified by GUIDE v2.5 08-Dec-2018 19:12:46

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @TrialGui2_OpeningFcn, ...
                   'gui_OutputFcn',  @TrialGui2_OutputFcn, ...
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

%% Our Code
% --- Executes just before TrialGui2 is made visible.
function TrialGui2_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to TrialGui2 (see VARARGIN)

global s;
s = serial('COM7', 'BaudRate', 9600);
fopen(s);

% Choose default command line output for TrialGui2
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);


% UIWAIT makes TrialGui2 wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = TrialGui2_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

%% Graph
% --- Executes during object creation, after setting all properties.
function Graph_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Graph (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: place code in OpeningFcn to populate Graph
HRValue=handles.HRVAL %Setting Heartrate
POSITION=handles.POSITION
x=[1:10];
y=[5,5,5,5,5,5,5,5,5,5];
if POSITION=='1'
    [x,y]=SVC_v2_synthetic(HRValue) %Superior Vena Cava
elseif POSITION=='2'
    [x,y]=highRA_v2(HRValue) %High Right Atrium
elseif POSITION=='3'
    [x,y]=midRA_v2(HRValue) %Mid Right Atrium
elseif POSITION=='4'
    [x,y]=lowRA_v2(HRValue) %Low Right Atrium
elseif POSITION=='5'
    [x,y]=RV_v2(HRValue) %Right Ventricle
elseif POSITION=='6'
    [x,y]=RVwall_v2(HRValue) %Right Ventricle
elseif POSITION=='7'
    [x,y]=PA_v2(HRValue) %Pulmonary Artery
elseif POSITION=='8'
    [x,y]=IVC_v2(HRValue) %Inferior Vena Cava
end
for i=1:length(x) 
    plot(x(1:i),y(1:i),'k','LineWidth',4);
    xlabel('Time (s)')
    ylabel('Amplitude (mA)')
    grid on
    set(gca,'Xlim',[min(x) 2],'Ylim',[0 1]);
    pause(0.01)
end
title('ECG')


%% BPM Input
function HRVal_Callback(hObject, eventdata, handles)
% hObject    handle to HRVal (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of HRVal as text
%        str2double(get(hObject,'String')) returns contents of HRVal as a double
HRVAL=str2double(get(hObject,'String'));
handles.HRVAL=HRVAL;

handles.POSITION = '0';

global s;

if (s.BytesAvailable >= 1)
    handles.POSITION = fscanf(s, '%c', 1)
end

Graph_CreateFcn([],[],handles);


% --- Executes during object creation, after setting all properties.
function HRVal_CreateFcn(hObject, eventdata, handles)
% hObject    handle to HRVal (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

%% Quit Button
function quitbutton_Callback(hObject, eventdata, handles)
% hObject    handle to quitbutton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

if ~isempty(instrfind)
    fclose(instrfind);
    delete(instrfind);
end

close(TrialGui2);
