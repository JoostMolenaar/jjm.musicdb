<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

    <xsl:output omit-xml-declaration="yes"/>

    <xsl:template match="/">
        <xsl:apply-templates select="/artist"/>
    </xsl:template>

    <xsl:template match="/artist">
        <form method="post">
            <xsl:attribute name="action">
                <xsl:value-of select="uri"/>
            </xsl:attribute>

            <xsl:choose>
                <xsl:when test="@mode = 'add'">
                    <h1>Add artist</h1>
                </xsl:when>
                <xsl:otherwise>
                    <h1>Update artist</h1>
                </xsl:otherwise>
            </xsl:choose>

            <label for="Name">Name</label>
            <input type="text" name="ArtistName">
                <xsl:attribute name="value">
                    <xsl:value-of select="name"/>
                </xsl:attribute>
            </input>

            <label for="Alias">Alias for</label>
            <select name="AliasID">
				<option>&#x2002;</option>
				<xsl:for-each select="/artist/available/artist">
					<xsl:call-template name="ArtistAlias">
						<xsl:with-param name="artistID" select="@artistID"/>
					</xsl:call-template>
				</xsl:for-each>
            </select>

            <label for="GroupID">In groups</label>
            <select name="GroupID" multiple="multiple">
				<option>&#x2002;</option>
				<xsl:for-each select="/artist/available/artist">
					<xsl:call-template name="ArtistGroups">
						<xsl:with-param name="artistID" select="@artistID"/>
					</xsl:call-template>
				</xsl:for-each>
            </select>

            <label/>
            <button name="add" type="submit">Add</button>
            <button name="update" type="submit">Update</button>
            <button name="delete" type="submit">Delete</button>
            <button name="cancel" type="reset">Cancel</button>
        </form>

		<xsl:if test="@mode = 'edit'">
			<img>
				<xsl:attribute name="src">
					<xsl:value-of select="/artist/img"/>
				</xsl:attribute>
			</img>
		</xsl:if>

	</xsl:template>

    <xsl:template name="ArtistAlias">
        <xsl:param name="artistID"/>
        <option>
            <xsl:attribute name="value">
                <xsl:value-of select="@artistID"/>
            </xsl:attribute>
            <xsl:if test="count(/artist/alias[@artistID=$artistID]) = 1">
                <xsl:attribute name="selected">
                    <xsl:text>selected</xsl:text>
                </xsl:attribute>
            </xsl:if>
            <xsl:value-of select="@name"/>
        </option>
    </xsl:template>
	
    <xsl:template name="ArtistGroups">
        <xsl:param name="artistID"/>
        <option>
            <xsl:attribute name="value">
                <xsl:value-of select="@artistID"/>
            </xsl:attribute>
            <xsl:if test="count(/artist/groups/artist[@artistID=$artistID]) = 1">
                <xsl:attribute name="selected">
                    <xsl:text>selected</xsl:text>
                </xsl:attribute>
            </xsl:if>
            <xsl:value-of select="@name"/>
        </option>
    </xsl:template>

</xsl:stylesheet>