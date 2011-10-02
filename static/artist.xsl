<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

    <xsl:template match="artists">
        <ul id="ArtistList">
            <xsl:apply-templates select="artist"/>
        </ul>
    </xsl:template>

    <xsl:template match="artist">
        <li>
            <a>
                <xsl:attribute name="href">
                    <xsl:value-of select="@uri"/>
                </xsl:attribute>
                <xsl:value-of select="@name"/>
            </a>
            <xsl:text> </xsl:text>
            <a class="small">
                <xsl:attribute name="href">
                    <xsl:value-of select="@uri"/>
                    <xsl:text>?xslt=artist_form.xsl</xsl:text>
                </xsl:attribute>
                <xsl:text>edit</xsl:text>
            </a>
        </li>
    </xsl:template>

</xsl:stylesheet>