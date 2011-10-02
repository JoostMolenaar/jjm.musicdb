<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

    <xsl:output omit-xml-declaration="yes"/>

    <xsl:template match="/">
        <xsl:apply-templates select="/release"/>
    </xsl:template>

    <xsl:template match="/release">
        <form method="post">
            <xsl:attribute name="action">
                <xsl:value-of select="uri"/>
            </xsl:attribute>

            <xsl:choose>
                <xsl:when test="@mode = 'edit'">
                    <h1>Update release</h1>
                </xsl:when>
                <xsl:otherwise>
                    <h1>Add release</h1>
                </xsl:otherwise>
            </xsl:choose>

            <!-- ReleaseName -->
            <label for="ReleaseName">Name</label>
            <input type="text" name="ReleaseName">
                <xsl:attribute name="value">
                    <xsl:value-of select="name"/>
                </xsl:attribute>
            </input>

            <!-- ArtistID -->
            <label for="ArtistID">Artist</label>
            <select name="ArtistID" multiple="multiple">
                <xsl:call-template name="ArtistOptions"/>
            </select>

            <!-- LabelID -->
            <label for="LabelID">Label</label>
            <select name="LabelID">
                <xsl:call-template name="LabelOptions">
                    <xsl:with-param name="LabelID" select="label/@labelID"/>
                </xsl:call-template>
            </select>

            <!-- CatNo -->
            <label for="CatNo">Cat.No</label>
            <input type="text" name="CatNo">
                <xsl:attribute name="value">
                    <xsl:value-of select="catno"/>
                </xsl:attribute>
            </input>

            <!-- Year -->
            <label for="Year">Year</label>
            <input type="text" name="Year">
                <xsl:attribute name="value">
                    <xsl:value-of select="year"/>
                </xsl:attribute>
            </input>

            <!-- FormatID -->
            <label for="FormatID">Format</label>
            <select name="FormatID">
                <xsl:call-template name="FormatOptions">
                    <xsl:with-param name="FormatID" select="format/@formatID"/>
                </xsl:call-template>
            </select>

            <label/>
            <button name="add" type="submit">Add</button>
            <button name="update" type="submit">Update</button>
            <button name="delete" type="submit">Delete</button>
            <button name="cancel" type="reset">Cancel</button>

            <!--label/>
            <a id="DiscogsLink" href="#">Discogs</a>
            <div id="DiscogsResults"/-->
        </form>
    </xsl:template>

    <xsl:template name="ArtistOptions">
        <option>&#x2002;</option>
        <xsl:for-each select="/release/artist">
            <xsl:call-template name="ArtistOption">
                <xsl:with-param name="artistID" select="@artistID"/>
                <xsl:with-param name="count">1</xsl:with-param>
            </xsl:call-template>
        </xsl:for-each>
        <xsl:for-each select="/release/available/artist">
            <xsl:call-template name="ArtistOption">
                <xsl:with-param name="artistID" select="@artistID"/>
                <xsl:with-param name="count">0</xsl:with-param>
            </xsl:call-template>
        </xsl:for-each>
    </xsl:template>

    <xsl:template name="ArtistOption">
        <xsl:param name="artistID"/>
        <xsl:param name="count"/>
        <xsl:if test="count(/release/artist[@artistID=$artistID]) = $count">
            <option>
                <xsl:attribute name="value">
                    <xsl:value-of select="@artistID"/>
                </xsl:attribute>
                <xsl:if test="$count = 1">
                    <xsl:attribute name="selected">
                        <xsl:text>selected</xsl:text>
                    </xsl:attribute>
                </xsl:if>
                <xsl:value-of select="/release/available/artist[@artistID=$artistID]/@name"/>
            </option>
        </xsl:if>
    </xsl:template>

    <xsl:template name="LabelOptions">
        <xsl:param name="LabelID"/>
        <xsl:for-each select="/release/available/label">
            <option>
                <xsl:attribute name="value">
                    <xsl:value-of select="@labelID"/>
                </xsl:attribute>
                <xsl:if test="@labelID = $LabelID">
                    <xsl:attribute name="selected">
                        <xsl:text>selected</xsl:text>
                    </xsl:attribute>
                </xsl:if>
                <xsl:value-of select="@name"/>
            </option>
        </xsl:for-each>
    </xsl:template>

    <xsl:template name="FormatOptions">
        <xsl:param name="FormatID"/>
        <xsl:for-each select="/release/available/format">
            <option>
                <xsl:attribute name="value">
                    <xsl:value-of select="@formatID"/>
                </xsl:attribute>
                <xsl:if test="@formatID = $FormatID">
                    <xsl:attribute name="selected">
                        <xsl:text>selected</xsl:text>
                    </xsl:attribute>
                </xsl:if>
                <xsl:value-of select="@name"/>
            </option>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>