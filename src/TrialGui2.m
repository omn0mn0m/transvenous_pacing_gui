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

% Last Modified by GUIDE v2.5 06-Nov-2018 14:26:00

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


% --- Executes just before TrialGui2 is made visible.
function TrialGui2_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to TrialGui2 (see VARARGIN)

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


% --- Executes during object creation, after setting all properties.
function Graph_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Graph (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called
% Hint: place code in OpeningFcn to populate Graph
x=0.01:0.01:2;
y=0; %initializing
val=handles
if strcmp(hObject,'svc')==1
    y=ecgsvc(val);
elseif strcmp(hObject,'hra')==1
    [x,y]=highRA_v2(val);
    x=x;
    y=y;
elseif strcmp(hObject,'mra')==1
    [x,y]=midRA_v2(val);
    x=x;
    y=y;
elseif strcmp(hObject,'lra')==1
    [x,y]=lowRA_v2(val);
    x=x;
    y=y;
elseif strcmp(hObject,'hrv')==1
    y=ecghrv(val);
elseif strcmp(hObject,'mrv')==1
    y=ecgmrv(val);
elseif strcmp(hObject,'lrv')==1
    y=ecglrv(val);
elseif strcmp(hObject,'pa')==1
    y=ecgpa(val);
elseif strcmp(hObject,'quit')==1
    x=0;
    y=0;
end
%curve=animatedline;
grid on
%z=0;
yvals=y;
xvals=x;
if y~=0
while strcmp(hObject,'pa')~=1
for i=1:length(x)  

plot(x(1:i),y(1:i),'k','LineWidth',4);
    xlabel('Time (s)')
    ylabel('Amplitude (mV)')
    grid on
    set(gca,'Xlim',[min(x) 2],'Ylim',[0 1]);
    pause(0.01)
end
end
end
xlabel('Time (s)')
ylabel('Amplitude (mV)')
title('ECG')
%end
%plot(x,y)
%xlabel('Time (s)');
%ylabel('Amplitude (mA)');
%title('ECG')


%options

% --- Executes on button press in svc.
function svc_Callback(hObject, eventdata, handles)
% hObject    handle to svc (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
Graph_CreateFcn('svc',[],handles.egg)


% --- Executes on button press in hra.
function hra_Callback(hObject, eventdata, handles)
% hObject    handle to hra (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
Graph_CreateFcn('hra')


% --- Executes on button press in mra.
function mra_Callback(hObject, eventdata, handles)
% hObject    handle to mra (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
Graph_CreateFcn('mra')


% --- Executes on button press in lra.
function lra_Callback(hObject, eventdata, handles)
% hObject    handle to lra (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
Graph_CreateFcn('lra')


% --- Executes on button press in hrv.
function hrv_Callback(hObject, eventdata, handles)
% hObject    handle to hrv (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
Graph_CreateFcn('hrv')

% --- Executes on button press in mrv.
function mrv_Callback(hObject, eventdata, handles)
% hObject    handle to mrv (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
Graph_CreateFcn('mrv')



function inputsvcval_Callback(hObject, eventdata, handles)
% hObject    handle to inputsvcval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of inputsvcval as text
%        str2double(get(hObject,'String')) returns contents of inputsvcval as a double
egg=str2double(get(hObject,'String'))
handles.egg=egg
Graph_CreateFcn('svc',[],handles.egg)

% --- Executes during object creation, after setting all properties.
function inputsvcval_CreateFcn(hObject, eventdata, handles)
% hObject    handle to inputsvcval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function inputhraval_Callback(hObject, eventdata, handles)
% hObject    handle to inputhraval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of inputhraval as text
%        str2double(get(hObject,'String')) returns contents of inputhraval as a double
egg=str2double(get(hObject,'String'))
handles.egg=egg
Graph_CreateFcn('hra',[],handles.egg)


% --- Executes during object creation, after setting all properties.
function inputhraval_CreateFcn(hObject, eventdata, handles)
% hObject    handle to inputhraval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function inputmraval_Callback(hObject, eventdata, handles)
% hObject    handle to inputmraval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of inputmraval as text
%        str2double(get(hObject,'String')) returns contents of inputmraval as a double
egg=str2double(get(hObject,'String'))
handles.egg=egg
Graph_CreateFcn('mra',[],handles.egg)

% --- Executes during object creation, after setting all properties.
function inputmraval_CreateFcn(hObject, eventdata, handles)
% hObject    handle to inputmraval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function inputlraval_Callback(hObject, eventdata, handles)
% hObject    handle to inputlraval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of inputlraval as text
%        str2double(get(hObject,'String')) returns contents of inputlraval as a double
egg=str2double(get(hObject,'String'))
handles.egg=egg
Graph_CreateFcn('lra',[],handles.egg)

% --- Executes during object creation, after setting all properties.
function inputlraval_CreateFcn(hObject, eventdata, handles)
% hObject    handle to inputlraval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function inputhrvval_Callback(hObject, eventdata, handles)
% hObject    handle to inputhrvval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of inputhrvval as text
%        str2double(get(hObject,'String')) returns contents of inputhrvval as a double
egg=str2double(get(hObject,'String'))
handles.egg=egg
Graph_CreateFcn('hrv',[],handles.egg)

% --- Executes during object creation, after setting all properties.
function inputhrvval_CreateFcn(hObject, eventdata, handles)
% hObject    handle to inputhrvval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function inputmrvval_Callback(hObject, eventdata, handles)
% hObject    handle to inputmrvval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of inputmrvval as text
%        str2double(get(hObject,'String')) returns contents of inputmrvval as a double
egg=str2double(get(hObject,'String'))
handles.egg=egg
Graph_CreateFcn('mrv',[],handles.egg)

% --- Executes during object creation, after setting all properties.
function inputmrvval_CreateFcn(hObject, eventdata, handles)
% hObject    handle to inputmrvval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in lrv.
function lrv_Callback(hObject, eventdata, handles)
% hObject    handle to lrv (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in pa.
function pa_Callback(hObject, eventdata, handles)
% hObject    handle to pa (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)



function inputlrvval_Callback(hObject, eventdata, handles)
% hObject    handle to inputlrvval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of inputlrvval as text
%        str2double(get(hObject,'String')) returns contents of inputlrvval as a double
egg=str2double(get(hObject,'String'))
handles.egg=egg
Graph_CreateFcn('lrv',[],handles.egg)


% --- Executes during object creation, after setting all properties.
function inputlrvval_CreateFcn(hObject, eventdata, handles)
% hObject    handle to inputlrvval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function inputpaval_Callback(hObject, eventdata, handles)
% hObject    handle to inputpaval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of inputpaval as text
%        str2double(get(hObject,'String')) returns contents of inputpaval as a double
egg=str2double(get(hObject,'String'))
handles.egg=egg
Graph_CreateFcn('pa',[],handles.egg)

% --- Executes during object creation, after setting all properties.
function inputpaval_CreateFcn(hObject, eventdata, handles)
% hObject    handle to inputpaval (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in quit.
function quit_Callback(hObject, eventdata, handles)
% hObject    handle to quit (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
Graph_CreateFcn('close',[],[]);
quit TrialGui2



function quitbutton_Callback(hObject, eventdata, handles)
% hObject    handle to quitbutton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of quitbutton as text
%        str2double(get(hObject,'String')) returns contents of quitbutton as a double
egg=str2double(get(hObject,'String'))
handles.egg=egg
Graph_CreateFcn('quit',[],handles.egg)


% --- Executes during object creation, after setting all properties.
function quitbutton_CreateFcn(hObject, eventdata, handles)
% hObject    handle to quitbutton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
