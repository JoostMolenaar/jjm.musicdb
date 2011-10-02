<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <xsl:include href="artist.xsl"/>
    <xsl:include href="label.xsl"/>
    <xsl:include href="format.xsl"/>
    <xsl:include href="release.xsl"/>

    <xsl:template match="/musicDB">
        <html>
            <head>
                <title>MusicDB</title>
                <link rel="stylesheet" type="text/css" href="musicdb.css"/>
                <script type="text/javascript" src="jquery-1.4.2.js"/>
                <script type="text/javascript" src="jquery-ui-1.8.1.custom.js"/>
                <script type="text/javascript" src="jquery.tablesorter.js"/>
                <script type="text/javascript" src="musicdb.js"/>
            </head>
            <body>
                <div id="Menu">
                    <h1>Menu</h1>
                    <ul id="MenuList">
                        <li><a id="AddArtistLink" href="/musicdb/artist/new?xslt=artist_form.xsl">Add artist</a></li>
                        <li><a id="AddLabelLink" href="/musicdb/label/new?xslt=label_form.xsl">Add label</a></li>
                        <li><a id="AddFormatLink" href="/musicdb/format/new?xslt=format_form.xsl">Add format</a></li>
                        <li><a id="AddReleaseLink" href="/musicdb/release/new?xslt=release_form.xsl">Add release</a></li>
                        <li><a id="LoginLink" href="/musicdb/login">Login</a></li>
                        <li><a id="ShowAllLink" href=".">Show all</a></li>
                    </ul>

                    <h1>Artists</h1>
                    <xsl:apply-templates select="artists"/>

                    <h1>Labels</h1>
                    <xsl:apply-templates select="labels"/>

                    <h1>Formats</h1>
                    <xsl:apply-templates select="formats"/>
                </div>
                <div id="Main">
                    <xsl:apply-templates select="releases"/>
                </div>
                <div id="Forms"/>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>
