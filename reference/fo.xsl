<?xml version='1.0'?>
<!DOCTYPE xsl:stylesheet PUBLIC "-//Thomson Lab//DTD Unofficial XSL//EN"  
                         "xsl.dtd">  
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:fo="http://www.w3.org/1999/XSL/Format"
                version='1.0'>

 <xsl:import href="http://docbook.sourceforge.net/release/xsl/snapshot/fo/docbook.xsl"/>

 <xsl:import href="citation.xsl"/>
 <xsl:import href="biblio.xsl"/> 
 <xsl:import href="pagesetup.xsl"/>

 <xsl:param name="headers.on.blank.pages" select="0"/>
 <xsl:param name="footers.on.blank.pages" select="0"/>

 <xsl:param name="page.margin.top">0.3in</xsl:param>
 <xsl:param name="page.margin.bottom">0.40in</xsl:param>
 <xsl:param name="page.margin.inner">0.60in</xsl:param>
 <xsl:param name="page.margin.outer">0.70in</xsl:param>
 <xsl:param name="body.margin.top">0.5in</xsl:param>
 <xsl:param name="body.margin.bottom">0.5in</xsl:param>

 <xsl:param name="body.font.family">Helvetica</xsl:param>
 <xsl:param name="title.font.family">Helvetica</xsl:param>
 <xsl:param name="monospace.font.family">Courier</xsl:param>
 <xsl:param name="sans.font.family">Helvetica</xsl:param>
 <xsl:param name="dingbat.font.family">Times Roman</xsl:param>

 <xsl:param name="title.margin.left" select="'0.0in'"/>
 <xsl:param name="toc.indent.width" select="8"/>

 <xsl:param name="insert.xref.page.number" select="1"/>

 <!-- page citation in format (see p.45) -->
 <xsl:param name="local.l10n.xml" select="document('')"/> 
 <l:i18n xmlns:l="http://docbook.sourceforge.net/xmlns/l10n/1.0"> 
  <l:l10n language="en"> 
   <l:context name="xref"> 
    <l:template name="page.citation" text=" (see p.%p)"/>
   </l:context>    
  </l:l10n>
 </l:i18n>

 <xsl:template match="varname">
  <xsl:call-template name="inline.italicseq"/>
 </xsl:template>

 <xsl:template match="application">
  <xsl:call-template name="inline.monoseq"/>
 </xsl:template>

 <xsl:template match="phrase[@role='strong']">
  <xsl:call-template name="inline.boldseq"/>
 </xsl:template>

 <!-- if verbatim environment embedded inside a *table element -->
 <!-- we can't use shaded background, this is a workaround for a -->
 <!-- bug in PassiveTeX -->
 <xsl:template match="programlisting[ancestor::entry]|screen[ancestor::entry]|synopsis[ancestor::entry]">
  <xsl:param name="suppress-numbers" select="'0'"/>

  <xsl:variable name="id"><xsl:call-template name="object.id"/></xsl:variable>
  
  <xsl:variable name="content">
   <xsl:choose>
    <xsl:when test="$suppress-numbers = '0'
     and @linenumbering = 'numbered'
     and $use.extensions != '0'
     and $linenumbering.extension != '0'">
     <xsl:call-template name="number.rtf.lines">
      <xsl:with-param name="rtf">
            <xsl:apply-templates/>
      </xsl:with-param>
     </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
     <xsl:apply-templates/>
    </xsl:otherwise>
   </xsl:choose>
  </xsl:variable>
  
  <xsl:choose>
   <xsl:when test="$shade.verbatim != 0">
    <!-- we check the for shaded flag, but don't use the attrib-set -->
    <fo:block  wrap-option='no-wrap'
     white-space-collapse='false'
     linefeed-treatment="preserve"    
     xsl:use-attribute-sets="monospace.verbatim.properties">
     <!-- normally part of use-attribute-sets: shade.verbatim.style -->
    <xsl:copy-of select="$content"/>
    </fo:block> 

   </xsl:when>
   <xsl:otherwise>
    
    <fo:block  wrap-option='no-wrap'
     white-space-collapse='false'
     linefeed-treatment="preserve"
     xsl:use-attribute-sets="monospace.verbatim.properties">
    
     <xsl:copy-of select="$content"/>
    </fo:block>
 
  </xsl:otherwise>
  </xsl:choose>
 </xsl:template>
 
</xsl:stylesheet>

<!--
Local variables:
mode:xml
sgml-local-catalogs: ("catalog")
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
