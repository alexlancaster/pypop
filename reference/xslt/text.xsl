<?xml version='1.0'?>

<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                version='1.0'>

 <xsl:import href="http://docbook.sourceforge.net/release/xsl/snapshot/html/docbook.xsl"/>

 <!-- import regular HTML customization -->
<!--  <xsl:import href="html.xsl"/>-->

 <xsl:import href="citation.xsl"/>
 <xsl:import href="biblio.xsl"/>


 <!-- now override some things we do/don't want in plaintext -->
 <xsl:param name="callout.unicode" select="'0'"/>
 <xsl:param name="callout.graphics" select="'0'"/>
 <xsl:param name="generate.toc"></xsl:param>

 <xsl:param name="appendix.autolabel" select="0"/>

 <!-- put quotes around only inline <para> userinput and filename -->
 <xsl:template match="para/userinput">
  <xsl:text>"</xsl:text>
  <xsl:call-template name="inline.boldmonoseq"/>
  <xsl:text>"</xsl:text>
 </xsl:template>

 <xsl:template match="para/filename">
  <xsl:text>"</xsl:text>
  <xsl:call-template name="inline.monoseq"/>
  <xsl:text>"</xsl:text>
 </xsl:template>

 <!-- put border around verbatim env -->
 <xsl:attribute-set name="shade.verbatim.style">
  <xsl:attribute name="border">1</xsl:attribute>
  <xsl:attribute name="bgcolor">#E0E0E0</xsl:attribute>
 </xsl:attribute-set>

 <!-- template to repeat a $string, $count times -->
 <xsl:template name="duplicate">
  <xsl:param name="string"/>
  <xsl:param name="count" select="1"/>

  <xsl:choose>
   <xsl:when test="not($count) or not($string)"/>
   <xsl:when test="$count = 1">
    <xsl:value-of select="$string"/>
   </xsl:when>
   <xsl:otherwise>
    <xsl:if test="$count mod 2">
     <xsl:value-of select="$string"/>
    </xsl:if>

    <xsl:call-template name="duplicate">
     <xsl:with-param name="string" select="concat($string,$string)"/>
     <xsl:with-param name="count" select="floor($count div 2)"/>
    </xsl:call-template>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

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

<!--
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
-->
   
    <xsl:copy-of select="$title"/>
    <!-- after title, output a break then some text highlighting -->
    <br/>
   
   <!-- if <h1> output '=', if <h2> or below, use '-' -->
    <xsl:call-template name="duplicate">
    <xsl:with-param name="string">
     <xsl:choose>
      <xsl:when test="($hlevel = 1) or ($hlevel = 2)">=</xsl:when>
      <xsl:otherwise>-</xsl:otherwise>
     </xsl:choose>
    </xsl:with-param>
    <xsl:with-param name="count" select="string-length($title)"/>
   </xsl:call-template>

<!--
  </xsl:element>
-->
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
