<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

    <xsl:template match="releases">
        <table id="ReleaseTable">
            <thead>
                <tr>
                    <th>Artist</th>
                    <th>Release</th>
                    <th>Ft</th>
                    <th>Label</th>
                    <th>Cat#</th>
                    <th>Year</th>
                </tr>
            </thead>
            <tbody>
                <xsl:apply-templates select="release"/>
            </tbody>
        </table>
    </xsl:template>

    <xsl:template match="release">
        <tr>
            <td>
                <xsl:call-template name="artistsref"/>
            </td>
            <td>
                <a>
                    <xsl:attribute name="href">
                        <xsl:value-of select="@uri"/>
                        <xsl:text>?xslt=release_form.xsl</xsl:text>
                    </xsl:attribute>
                    <xsl:value-of select="@name"/>
                </a>
            </td>
            <td>
                <xsl:call-template name="ref">
                    <xsl:with-param name="ref" select="@format"/>
                </xsl:call-template>
            </td>
            <td>
                <xsl:call-template name="ref">
                    <xsl:with-param name="ref" select="@label"/>
                </xsl:call-template>
            </td>
            <td><xsl:value-of select="@cat"/></td>
            <td><xsl:value-of select="@year"/></td>
        </tr>
    </xsl:template>

    <xsl:template name="artistsref">
        <xsl:for-each select="a">
            <xsl:if test="position() != 1">
                <xsl:text>/</xsl:text>
            </xsl:if>
            <xsl:call-template name="ref">
                <xsl:with-param name="ref" select="@ref"/>
            </xsl:call-template>
        </xsl:for-each>
    </xsl:template>

    <xsl:template name="ref">
        <xsl:param name="ref"/>
        <xsl:for-each select="/musicDB/*/*[@uri=$ref]">
            <a>
                <xsl:attribute name="href">
                    <xsl:value-of select="@uri"/>
                </xsl:attribute>
                <xsl:value-of select="@name"/>
            </a>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>