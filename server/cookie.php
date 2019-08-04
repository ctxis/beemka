<?php
// Change these settings if you need to.
$storage = '/tmp/beemka-cookies.txt';
$paramUrl = 'url';
$paramData = 'data';

class CookieStorage {
    protected $storage = '';

    public function __construct($storage)
    {
        $this->storage = $storage;
        $this->setup();
    }

    protected function setup()
    {
        if (!file_exists($this->storage)) {
            @touch($this->storage);
        }

        if (!file_exists($this->storage)) {
            throw new Exception("Could not create storage file");
        } elseif (!is_writable($this->storage)) {
            throw new Exception("Storage file is not writable");
        }
    }

    public function saveCookie($url, $data)
    {
        $text = time() . '|' . base64_encode($url) . '|' . base64_encode($data);
        return file_put_contents($this->storage, $text . PHP_EOL, FILE_APPEND);
    }

    public function getCookies()
    {
        $data = array_filter(
            explode(PHP_EOL, file_get_contents($this->storage)),
            function($c) {
                return !empty($c);
            }
        );

        $cookies = [];
        foreach ($data as $line) {
            $info = explode('|', $line);
            $time = $info[0];
            $url = base64_decode($info[1]);
            $cookie = base64_decode($info[2]);

            if (!isset($cookies[$time])) {
                $cookies[$time] = [];
            }

            $cookies[$time][] = (object)[
                'url' => $url,
                'cookie' => $cookie
            ];
        }

        return $cookies;
    }

    public function clearCookies()
    {
        @unlink($this->storage);
    }
}

$cookieStorage = new CookieStorage($storage);
if (isset($_REQUEST['clear'])) {
    $cookieStorage->clearCookies();
    header('Location: ' . basename(__FILE__));
    die();
}

$url = isset($_REQUEST[$paramUrl]) ? trim($_REQUEST[$paramUrl]) : '';
$data = isset($_REQUEST[$paramData]) ? trim($_REQUEST[$paramData]) : '';

if (!empty($url) && !empty($data)) {
    $cookieStorage->saveCookie($url, $data);
    die();
}

$allCookies = $cookieStorage->getCookies();
?>
<html>
<head>
    <title>Beemka Cookie Viewer</title>

    <style type="text/css">
        body {
            font-family: "Verdana";
        }

        .container {
            width: 1200px;
            height: 100%;
            margin: auto;
        }

        .left {
            width: 500px;
            height: 100%;
            float: left;
            overflow: auto;
        }

        .right {
            margin-left: 500px;
            width: 700px;
            height: 100%;
            overflow: auto;
        }

        h1 {
            margin: 0;
            padding: 0;
            font-size: 1.2em;
        }

        .index ul.top {
            list-style-type: none;
            padding: 0;
        }

        .clear-cookies {
            font-size: 0.7em;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="left">
        <h1>Cookies <span class="clear-cookies"><a href="<?php echo basename(__FILE__); ?>?clear">clear</a></span></h1>

        <div class="index">
            <ul class="top">
            <?php foreach ($allCookies as $time => $data) { ?>
                <li>
                    <p><a class="cookie-time" href="#" data-time="<?php echo $time; ?>"><?php echo date('Y-m-d H:i:s', $time); ?></a></p>
                    <ul id="cookie-<?php echo $time; ?>" style="display: none;" class="bottom">
                    <?php foreach ($data as $cookie) { ?>
                        <li><a class="cookie-link" href="#" data-cookie="<?php echo base64_encode($cookie->cookie); ?>"><?php echo $cookie->url; ?></a></li>
                    <?php } ?>
                    </ul>
                </li>
            <?php } ?>
            </ul>
        </div>
    </div>
    <div class="right">
        <h1>Contents</h1>

        <pre id="cookie-contents"></pre>
    </div>
</div>

<script type="text/javascript">
    function attachEvent(className, eventName, callbackFunction) {
        var elements = document.getElementsByClassName(className);
        for (var i = 0; i < elements.length; i++) {
            elements[i].addEventListener(eventName, callbackFunction);
        }
        return true;
    }

    function clickTime(event) {
        var list = document.getElementById('cookie-' + this.getAttribute('data-time'));
        display = (list.style.display == '') ? 'none' : '';
        list.style.display = display;
        event.preventDefault();
    }

    function clickLink(event) {
        var data = atob(this.getAttribute('data-cookie'));
        document.getElementById('cookie-contents').innerText = data;
        event.preventDefault();
    }

    attachEvent('cookie-time', 'click', clickTime);
    attachEvent('cookie-link', 'click', clickLink);
</script>
</body>
</html>
