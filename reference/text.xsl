<?xml version='1.0'?>

<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version='1.0'>

 <!-- import regular HTML customization -->
 <xsl:import href="html.xsl"/>

 <!-- now override some things we do/don't want in plaintext -->
 <xsl:param name="callout.unicode" select="'0'"/>
 <xsl:param name="callout.graphics" select="'0'"/>
 <xsl:param name="param generate.toc"></xsl:param>

 <xsl:template name="section.heading">
  <xsl:param name="section" select="."/>
  <xsl:param name="level" select="1"/>
  <xsl:param name="allow-anchors" select="1"/>
  <xsl:param name="title"/>
  <xsl:param name="class" select="'title'"/>

  <xsl:variable name="id">
    <xsl:choose>
      <!-- if title is in an *info wrapper, get the grandparent -->
      <xsl:when test="contains(local-name(..), 'info')">
        <xsl:call-template name="object.id">
          <xsl:with-param name="object" select="../.."/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="object.id">
          <xsl:with-param name="object" select=".."/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <!-- HTML H level is one higher than section level -->
  <xsl:variable name="hlevel" select="$level + 1"/>
  <xsl:element name="h{$hlevel}">
    <xsl:attribute name="class"><xsl:value-of select="$class"/></xsl:attribute>
    <xsl:if test="$css.decoration != '0'">
      <xsl:if test="$hlevel&lt;3">
        <xsl:attribute name="style">clear: both</xsl:attribute>
      </xsl:if>
    </xsl:if>
    <xsl:if test="$allow-anchors != 0">
      <xsl:call-template name="anchor">
        <xsl:with-param name="node" select="$section"/>
        <xsl:with-param name="conditional" select="0"/>
      </xsl:call-template>
    </xsl:if>
    <xsl:copy-of select="$title"/>

  </xsl:element>
</xsl:template>

 
</xsl:stylesheet>

<!--
Local variables:
mode:xml
sgml-indent-step: 1
sgml-indent-data: 1
sgml-default-dtd-file: "../../src/xslt/xsl.ced"
sgml-local-catalogs: ("catalog")
End:
-->
