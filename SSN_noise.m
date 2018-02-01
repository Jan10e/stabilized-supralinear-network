% author:              Jantine Broek
% collaborator:     Yashar Ahmadian
% goal:                 recreate E-I 2D model of Hennequin add noise and so simulate data of Kohn&Cohen. 
%                          We focused on analysing how the intrinsic dynamics of the network shaped external noise
%                          to give rise to stimulus dependent patterns of response variability.
% model:              stabilized supralinear network model with OU process
%                          (noise added per dt)

%% OUP for noise
% with Wiener increments and ``scaled-time transformed'' Wiener process
% This is a Forcing term for the dynamical model
clear all, close all

th = 1;
mu = 0;                                 % mu to 0 as it needs to decay to 0
sig = 0.3;
dt = 1e-4;
t = 0:dt:20;                             % Time vector
x0 = 1;                                 % Set initial condition (not 0, otherwise you don't see it decaying to 0)
rng(1);                                  % Set random seed

% create two processes: one for E population and one for I population
W = zeros(2,length(t));        % Allocate integrated W vector

for ii = 1:length(t)-1
    W(:,ii+1) = W(:,ii)+sqrt(exp(2*th*t(:,ii+1))-exp(2*th*t(:,ii)))*randn(2,1);
end

ex = exp(-th*t);
x = x0*ex+mu*(1-ex)+sig*ex.*W/sqrt(2*th);

%figure;
plot(t,x);

%% Euler method forward method + noise W

% Vm for neuron E and I
u_0 = [-60; -80]; %-80 for E, 60 for I
%tend = 1;

% Euler loop
u = zeros(2,length(W));
u(:,1) = u_0;
for ii = 1: length(W)-1
    
      % Take the Euler step + x(i) which is the noise
      u(:,ii+1) = u(:,ii) + ssn_ode(t, (u(:,ii) + x(:,ii)))*dt;
      
end

figure;
plot(t, u)

% stds = [];
% h_range = (0:0.5:20);
% for n = h_range
%     
%     % update input
%     disp(n)
%     h = ones(2) * n;
%     
%     %get time vector
% %     count = (1:1:length(u));
% %     t = [count; u]';
%     
%     for m = 1: length(u)-1
%     
%       % Take the Euler step + x(i) which is the noise
%       u(:,m+1) = u_0 + ssn_ode(t, u(:,m))*dt + (x(:,m)*0);
%       
%     end
%     
%     %stds = append(std(u(:,n)));
%     stds = std(u);
%       
% end

%% Sanity check
% look how this works for variaous tau > when tau is really small and big

