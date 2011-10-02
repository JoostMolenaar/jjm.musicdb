<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0">

    <xsl:template match="/">
        <xsl:apply-templates select="/format"/>
    </xsl:template>

    <xsl:template match="/format">
        <form method="post">
            <xsl:attribute name="action">
                <xsl:value-of select="uri"/>
            </xsl:attribute>

            <xsl:choose>
                <xsl:when test="@mode = 'edit'">
                    <h1>Update format</h1>
                </xsl:when>
                <xsl:otherwise>
                    <h1>Add format</h1>
                </xsl:otherwise>
            </xsl:choose>

            <label for="Name">Name</label>
            <input type="text" name="FormatName">
                <xsl:attribute name="value">
                    <xsl:value-of select="name"/>
                </xsl:attribute>
            </input>

            <label/>
            <button name="add" type="submit">Add</button>
            <button name="update" type="submit">Update</button>
            <button name="delete" type="submit">Delete</button>
            <button name="cancel" type="reset">Cancel</button>
        </form>
    </xsl:template>
</xsl:stylesheet>