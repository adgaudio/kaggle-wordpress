<?php

require_once("facebook.php");

$config = array();
$config['appId'] = '343180059059629';
$config['secret'] = 'e0556149e87049fbfe6e236396f3c1dd';

$facebook = new Facebook($config);

$user = $facebook->getUser();
if($user && isset($_GET['getAccessToken'])){
echo $facebook->getAccessToken()
     .'<br /><br /><a href="http://kratsg.caltech.edu/public_html/fb/">Go back</a>';
die;
}

$loginUrl = $facebook->getLoginUrl();
$logoutUrl = $facebook->getLogoutUrl();
?>

<?php if ($user){?>
Logged In! Would you like to <a href="<?php echo $logoutUrl; ?>">logout</a>?
<?php }else if(!$user && isset($_GET['getAccessToken'])){ ?>
<div>
Login using OAuth 2.0 handled by the PHP SDK:
<a href="<?php echo $loginUrl; ?>">Login with Facebook</a>
</div>
<?php } ?>
<hr />
This uses the following python codes (save them to your computer!):
<ul>
    <li><a href="facebookrec.py">Facebook Recommendation</a></li>
    <li><a href="recommendations.py">Recommendations (required)</a></li>
</ul>
<i>facebookrec.py</i> is a python file - when you run it for the first time (use IDLE, interactive prompt, etc...), it should open up the web browser and require you to copy/paste the access token in. Once you do that, you can run it again (use IDLE!) and it will start fetching your likes and your friends and their likes. There are helper functions "get_recommendations(users,'Some Name')" and "get_topMatches(users,'Some Name')" which will fetch pages for you to like and people you are most compatible with based on likes. <br /><br /> Run the code like so:
<pre>
>>> recs = get_recommendations(users,me['name'])
>>> topFriends = get_topMatches(users,me['name'])
>>> recs[0:5]
# prints the top 5 recs
>>> topFriends[0:5]
# prints the top 5 friends
</pre>
<br />
If you find that the results aren't predictive of you, you can try the other similarity indexing I have (Euclidean Distance) by running:
<pre>
>>> recs_dis = get_recommendations(users,me['name'],similarity=sim_distance)
>>> topFriends_dis = get_topMatches(users,me['name'],similarity=sim_distance)
>>> recs_dis[0:5]
# prints the top 5 recs
>>> topFriends_dis[0:5]
# prints the top 5 friends
</pre>
<br />
But in most cases, it won't make a significant change in the results, but maybe the order of the top few.

