clc;
clear;
close all;

%%

fstats = load('stats_frame_tracking.txt');
pstats = load('stats_point_tracking.txt');
sstats = load('stats_optimization.txt');

%% frame tracking
figure;
subplot(2, 1, 1);
title('frame tracking stats');
hold on;
plot(fstats(:, 1), fstats(:, 3), 'LineWidth', 2, 'color', 'g');
hold on;
plot(fstats(:, 1), fstats(:, 4), 'LineWidth', 1, 'color', 'r');
grid on;
xlabel('iteration');
legend("number of proposed poses", "number of tried poses");

mean_frame_tracking_time = mean(fstats(:, 6))
subplot(2, 1, 2);
plot(fstats(:, 1), fstats(:, 6), 'LineWidth', 1, 'color', 'r');
grid on;
xlabel('iteration');
legend('frame tracking time (s)');

frame_outlier = sum(fstats(:, 4) > 1)

% subplot(4, 1, 3);
% plot(fstats(:, 1), fstats(:, 7), 'LineWidth', 0.1, 'color', 'r');
% grid on;
% xlabel('iteration');
% legend('is keyframe (true=1, false=0)');

%% point tracking
figure;
subplot(2, 1, 1);
title('point tracking stats');
hold on;
plot(pstats(:, 1), pstats(:, 2), 'color', 'r');
grid on;
xlabel('iteration');
legend("number of tracked points");

subplot(2, 1, 2);
plot(pstats(:, 1), pstats(:, 3), 'color', 'r');
grid on;
xlabel('iteration');
ylabel('tracking time (s)');
legend('point tracking time');
mean_point_tracking_time = mean(pstats(:, 3))

%% sliding window optimization
figure;

% new_residual, new_points, opt, post, set_ref, marg_pts, new_traces,
% marg_frames
mean_swo_time = mean(sstats(:, 7:end))
mean_optimization_time = mean(sstats(:, 9))

subplot(5, 1, 1);
title('sliding window optimization stats');
hold on;
plot(sstats(:, 1), sstats(:, 3), 'r');
grid on;
xlabel('iteration');
legend('newly added points');

subplot(5, 1, 2);
plot(sstats(:, 1), sstats(:, 4), 'r');
grid on;
xlabel('iteration');
legend('number of keyframes');

subplot(5, 1, 3);
plot(sstats(:, 1), sstats(:, 5), 'r');
grid on;
xlabel('iteration');
legend('number of points');

subplot(5, 1, 4);
plot(sstats(:, 1), sstats(:, 6), 'r');
grid on;
xlabel('iteration');
legend('number of residuals');
mean_residual_number = mean(sstats(:, 6))

subplot(5, 1, 5);
plot(sstats(:, 1), sstats(:, 9), 'r');
grid on;
xlabel('iteration');
legend('optimization time (s)');

%% boxplot
fnum = size(fstats, 1);
pnum = size(pstats, 1);
snum = size(sstats, 1);
ty = [fstats(:, 6); pstats(:, 3); sstats(:, 9); sstats(:, 10)];
tx = [zeros(fnum, 1); ones(pnum, 1); ones(snum, 1) * 2; ones(snum, 1) * 3 ];
figure;
title('time cost (s): frame + point  + opt + post');
hold on;
boxplot(ty, tx);
grid on;
ylabel('seconds');
% legend('frame tracking', 'point tracking', 'optimization', 'post processing');

%% bar plot
figure;
title('time cost (ms)');
% bar1: opt + outlier + ref + marg_p + new_trace + marg_f
hold on;
colormap(cool);
view(90, 90);
bar([mean(sstats(:, [9, 11, 12, 13, 14, 15])); 0 0 0 0 0 0] * 1e3, 'stacked');
grid on;

figure;
title('frame tracking time')
hold on;
colormap(cool);
view(90, 90);
bar(mean(fstats(:, 6)) * 1e3, 'stacked'); % use ms
ylabel('ms');
grid on;

