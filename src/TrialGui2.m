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

close_serial;

% Handle variables
handles.s = serial('/dev/tty.usbmodem14203', 'BaudRate', 9600);
handles.HRVAL = 60;

global POSITION;
POSITION = '0';

global RUN;
RUN = 1;

handles.s.BytesAvailableFcnCount = 1;
handles.s.BytesAvailableFcnMode = 'byte';
handles.s.BytesAvailableFcn = {@serial_read_Callback, handles};

% handles.timer = timer(...
%     'ExecutionMode', 'fixedRate', ...
%     'Period', 0.5, ...
%     'TimerFcn', {@serial_read_Callback, handles});
% start(handles.timer);

% Choose default command line output for TrialGui2
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

fopen(handles.s);


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
global POSITION;
global HRValue;

while ~isempty(findobj('Name', 'TrialGui2'))
    %HRValue=handles.HRVAL; %Setting Heartrate

    switch POSITION
        case '0'
            x=[0:64];
            y=ones(64) * 1;
        case '1'
            [x,y]=SVC_v2_synthetic(HRValue); %Superior Vena Cava
        case '2'
            [x,y]=highRA_v2(HRValue); %High Right Atrium
        case '3'
            [x,y]=midRA_v2(HRValue); %Mid Right Atrium
        case '4'
            [x,y]=lowRA_v2(HRValue); %Low Right Atrium
        case '5'
            [x,y]=RV_v2(HRValue); %Right Ventricle
        case '6'
            [x,y]=RVwall_v2(HRValue); %Right Wall
        case '7'
            [x,y]=PA_v2(HRValue); %Pulmonary Artery
        case '8'
            [x,y]=IVC_v2(HRValue); %Inferior Vena Cava
        otherwise
            x=[0:64];
            y=ones(64) * -0.25;
    end

    for i=1:length(x) 
        plot(x(1:i),y(1:i),'k','LineWidth',3);
        xlabel('Time (s)')
        ylabel('Amplitude (mA)')
        grid on
        set(gca,'Xlim',[min(x) 2],'Ylim',[0 2]);
        pause(0.01)
    end
    title('ECG')
end

%% Serial Read
function serial_read_Callback(hObject, eventdata, handles)
% hObject    handle
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of HRVal as text
%        str2double(get(hObject,'String')) returns contents of HRVal as a double
% handles.POSITION = '0';
global POSITION;

if (handles.s.BytesAvailable >= 1)
    POSITION = fscanf(handles.s, '%c', 1)
end


%% BPM Input
function HRVal_Callback(hObject, eventdata, handles)
% hObject    handle to HRVal (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of HRVal as text
%        str2double(get(hObject,'String')) returns contents of HRVal as a double
global HRValue;
HRValue=str2double(get(hObject,'String'));
%handles.HRVAL=HRVAL;

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

close_serial;

close(TrialGui2);
