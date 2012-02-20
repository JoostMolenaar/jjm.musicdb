<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

    <xsl:template match="/">
        <xsl:apply-templates select="/label"/>
    </xsl:template>

    <xsl:template match="/label">
        <form method="post">
            <xsl:attribute name="action">
                <xsl:value-of select="uri"/>
            </xsl:attribute>

            <xsl:choose>
                <xsl:when test="@mode = 'edit'">
                    <h1>Update label</h1>
                </xsl:when>
                <xsl:otherwise>
                    <h1>Add label</h1>
                </xsl:otherwise>
            </xsl:choose>

            <label for="Name">Name</label>
            <input type="text" name="LabelName">
                <xsl:attribute name="value">
                    <xsl:value-of select="name"/>
                </xsl:attribute>
            </input>

            <label for="ParentID">Parent</label>
            <select name="ParentID">
				<option>&#x2002;</option>
				<xsl:for-each select="//available/label">
					<xsl:call-template name="LabelOption">
						<xsl:with-param name="labelID" select="@labelID"/>
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
					<xsl:value-of select="/label/img"/>
				</xsl:attribute>
			</img>
		</xsl:if>
    </xsl:template>
	
	<xsl:template name="LabelOption">
        <xsl:param name="labelID"/>
        <option>
            <xsl:attribute name="value">
                <xsl:value-of select="@labelID"/>
            </xsl:attribute>
            <xsl:if test="count(/label/parent[@labelID=$labelID]) = 1">
                <xsl:attribute name="selected">
                    <xsl:text>selected</xsl:text>
                </xsl:attribute>
            </xsl:if>
            <xsl:value-of select="@name"/>
        </option>
    </xsl:template>

</xsl:stylesheet>