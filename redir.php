<?php
// Get the URL parameter from the query string
$url = $_GET['url'];

// Get the status code parameter from the query string, default to 302 if not provided
$statusCode = isset($_GET['code']) ? intval($_GET['code']) : 302;

// List of supported status codes
$supportedStatusCodes = array(301, 302, 303, 307);

// Check if the provided status code is supported
if (!in_array($statusCode, $supportedStatusCodes)) {
    // If the provided status code is not supported, default to 302
    $statusCode = 302;
}

// Perform the redirect with the provided status code
header("Location: $url", true, $statusCode);
exit();
?>
