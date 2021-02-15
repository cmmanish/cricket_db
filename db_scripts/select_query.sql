Runs - select sum(runs_batsman) from odi_ball_by_ball_v2 where  batsman_name like'%Kohli%';

Balls - select count(runs_batsman) from odi_ball_by_ball_v2 where  batsman_name like'%Kohli%';

Runs vs bowler - select sum(runs_batsman) from odi_ball_by_ball_v2 where batsman_name like'%Kohli%' and bowler_name like '%Malinga%';

