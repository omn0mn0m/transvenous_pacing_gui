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

%s = Serial('/dev/tty.usbmodem14103', 'BaudRate', 9600);
%fopen(s);

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
HRValue=handles %Setting Heartrate
x=[1:10];
y=[5,5,5,5,5,5,5,5,5,5];
%z=0;
%yvals=y;
%xvals=x;
%if y~=0
% while strcmp(hObject,'pa')~=1
% for i=1:length(x)  
% 
% plot(x(1:i),y(1:i),'k','LineWidth',4);
%     xlabel('Time (s)')
%     ylabel('Amplitude (mV)')
%     grid on
%     set(gca,'Xlim',[min(x) 2],'Ylim',[0 1]);
%     pause(0.01)
% end
% end
%end
for i=1:length(x) 
    plot(x(1:i),y(1:i),'k','LineWidth',4);
    xlabel('Time (s)')
    ylabel('Amplitude (mA)')
    grid on
    set(gca,'Xlim',[1 10],'Ylim',[1 10]);
    pause(0.1)
end
title('ECG')
%end
%plot(x,y)

%% BPM Input
function HRVal_Callback(hObject, eventdata, handles)
% hObject    handle to HRVal (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of HRVal as text
%        str2double(get(hObject,'String')) returns contents of HRVal as a double
HRVAL=str2double(get(hObject,'String'));
handles.HRVAL=HRVAL;

if (s.BytesAvailable >= 1)
    temp = fscanf(s, '%c', 1)
end

Graph_CreateFcn([],[],handles.HRVAL);


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
close(TrialGui2);
% if ~isempty(instrfind)
%     fclose(instrfind);
%     delete(instrfind);
% end
