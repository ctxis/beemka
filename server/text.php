<?php
$storage = '/tmp/beemka-text.txt';

// Try to create file.
@touch($storage);
if (!file_exists($storage)) {
	die('Could not create storage file: ' . $storage);
} elseif (!is_writable($storage)) {
	die($storage . ' is not writable.');
}

$data = isset($_REQUEST['data']) ? trim($_REQUEST['data']) : '';
if (!empty($data)) {
	file_put_contents($storage, $data, FILE_APPEND);
	die();
}

$data = file_get_contents($storage);
?>
<html>
<head>
</head>
<body>
	<pre><?php echo $data; ?></pre>

	<script type="text/javascript">
        setInterval(
            function() {
                location.reload();
            },
            1000
        );
    </script>
</body>
</html>