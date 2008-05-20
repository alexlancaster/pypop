<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version='1.0'>

 <xsl:param name="latex.biblio.output">cited</xsl:param>
 <xsl:param name="insert.xref.page.number">no</xsl:param>

 <xsl:template match="biblioentry/title|biblioentry/citetitle">
  <xsl:choose>
   <xsl:when test="@pubwork='article'">
    <xsl:call-template name="dingbat">
     <xsl:with-param name="dingbat">ldquo</xsl:with-param>
    </xsl:call-template>
    <xsl:apply-templates/>
    <xsl:call-template name="dingbat">
     <xsl:with-param name="dingbat">rdquo</xsl:with-param>
    </xsl:call-template>
   </xsl:when>
   <xsl:when test="@pubwork='journal' or @pubwork='book'">
   <xsl:text>\emph{</xsl:text> 
    <xsl:apply-templates/>
    <xsl:text>}</xsl:text>
   </xsl:when>
   <xsl:otherwise>
    <xsl:text>\emph{</xsl:text> 
    <xsl:apply-templates/>
    <xsl:text>}</xsl:text> 
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>
 

<xsl:template name="biblioentry.output">
  <xsl:call-template name="bibitem"/>
  <!-- first, biblioentry information (if any) -->
  <xsl:variable name="data" select="subtitle|
                                    volumenum|
                                    edition|
                                    address|
                                    copyright|
                                    publisher|
                                    pubdate|
                                    pagenums|
                                    isbn|
                                    issn|
                                    biblioid|
                                    releaseinfo|
                                    pubsnumber"/>
  <xsl:apply-templates select="author|authorgroup" mode="bibliography.mode"/>
  <xsl:if test="citetitle or title">
   <xsl:if test="author|authorgroup">
    <xsl:value-of select="$biblioentry.item.separator"/>
    </xsl:if>
   <xsl:for-each select="citetitle|title">
    <xsl:apply-templates select="."/>
    <xsl:if test="position()!=last()">
     <xsl:text>, </xsl:text>
    </xsl:if>
   </xsl:for-each>
  </xsl:if>
  <!-- then, biblioset information (if any) -->
  <xsl:for-each select="biblioset">
   <!-- don't put blank lines between bibliosets -->
   <!-- <xsl:text>&#10;&#10;</xsl:text> -->
   <xsl:text> </xsl:text>
   <xsl:apply-templates select="." mode="bibliography.mode"/>
  </xsl:for-each>
  
  <!-- other stuff after biblioset -->
  <xsl:if test="$data">
    <xsl:for-each select="$data">
      <xsl:value-of select="$biblioentry.item.separator"/>
      <xsl:apply-templates select="." mode="bibliography.mode"/> 
    </xsl:for-each>
    <xsl:text>.</xsl:text>
  </xsl:if>

  <xsl:apply-templates select="bibliomisc" mode="bibliography.mode"/>
  <xsl:call-template name="label.id"/> 
  <xsl:text>&#10;</xsl:text>
</xsl:template>


<xsl:template match="biblioset" mode="bibliography.mode">
  <xsl:if test="author|authorgroup">
    <xsl:apply-templates select="author|authorgroup" mode="bibliography.mode"/>
    <xsl:value-of select="$biblioentry.item.separator"/>
  </xsl:if>
  <xsl:apply-templates select="title" mode="bibliography.mode"/>
  <xsl:apply-templates select="citetitle" mode="bibliography.mode"/>
  <xsl:for-each select="subtitle|
                        volumenum|
                        edition|
                        address|
                        copyright|
                        publisher|
                        pubdate|
                        pagenums|
                        isbn|
                        issn|
                        biblioid|
                        pubsnumber">
    <xsl:value-of select="$biblioentry.item.separator"/>
    <xsl:apply-templates select="." mode="bibliography.mode"/> 
  </xsl:for-each>
  <xsl:text>.</xsl:text>
</xsl:template>

<xsl:template match="title|citetitle" 
              mode="bibliography.mode">
  <xsl:variable name="relation" select="../@relation"/>
  <xsl:choose>
    <xsl:when test="$relation='article'">
      <xsl:call-template name="dingbat">
        <xsl:with-param name="dingbat">ldquo</xsl:with-param>
      </xsl:call-template>
      <xsl:apply-templates/>
      <xsl:call-template name="dingbat">
        <xsl:with-param name="dingbat">rdquo</xsl:with-param>
      </xsl:call-template>
    </xsl:when>
   <xsl:when test="$relation='journal' or $relation='book'">
   <xsl:text>\emph{</xsl:text> 
    <xsl:apply-templates/>
    <xsl:text>}</xsl:text>
   </xsl:when>
    <xsl:otherwise>
      <xsl:apply-templates/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>
