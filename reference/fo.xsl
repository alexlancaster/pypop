
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

 <xsl:param name="body.font.family">sans-serif</xsl:param>
 <xsl:param name="title.font.family">sans-serif</xsl:param>
 <xsl:param name="monospace.font.family">monospace</xsl:param>
 <xsl:param name="sans.font.family">sans-serif</xsl:param>
 <xsl:param name="dingbat.font.family">serif</xsl:param>

 <xsl:param name="title.margin.left" select="'0.0in'"/>
 <xsl:param name="toc.indent.width" select="8"/>

 <!-- callout format -->
 <xsl:param name="callout.unicode" select="'1'"/>
 <xsl:param name="callout.graphics" select="'0'"/>

 <!-- admon format -->
 <xsl:attribute-set name="admonition.properties">
  <xsl:attribute name="font-family">serif</xsl:attribute>
  <xsl:attribute name="font-style">italic</xsl:attribute>
  <xsl:attribute name="font-weight">bold</xsl:attribute>
 </xsl:attribute-set>

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

 <!-- make verbatim environments font-size 90% of main font size -->
 <xsl:attribute-set name="verbatim.properties">
  <xsl:attribute name="space-before.minimum">0.8em</xsl:attribute>
  <xsl:attribute name="space-before.optimum">1em</xsl:attribute>
  <xsl:attribute name="space-before.maximum">1.2em</xsl:attribute>
  <xsl:attribute name="space-after.minimum">0.8em</xsl:attribute>
  <xsl:attribute name="space-after.optimum">1em</xsl:attribute>
  <xsl:attribute name="space-after.maximum">1.2em</xsl:attribute>
  <xsl:attribute name="font-size">
   <xsl:value-of select="$body.font.master*0.9"/><xsl:text>pt</xsl:text></xsl:attribute>
 </xsl:attribute-set>

 <!-- workaround template for bugs in PassiveTeX which crop -->
 <!-- up in verbatim environments, exempt <screen> b/c workaround -->
 <!-- strips off useful markup for inline elements, <programlisting> -->
 <!-- is used for literal output with no inline elements -->

 <xsl:template match="programlisting|synopsis">
  <xsl:param name="suppress-numbers" select="'0'"/>
  
  <xsl:variable name="id"><xsl:call-template name="object.id"/></xsl:variable>
  
  <xsl:variable name="content">  

   <!-- replace ALL spaces with XML space character: &#160; -->
   <!-- because PassiveTeX, being braindead sometimes -->
   <!-- doesn't treat blank spaces and actual -->
   <!-- XML characters identically (grr) -->

   <xsl:call-template name="string.subst">
    <xsl:with-param name="target" select="' '"/>
    <xsl:with-param name="replacement" select="'&#160;'"/>
    <xsl:with-param name="string">

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
     
    </xsl:with-param>
   </xsl:call-template>
  </xsl:variable>

  <!-- if verbatim environment embedded inside a *table element -->
  <!-- we can't use shaded background, this is a workaround for a -->
  <!-- *another* bug in PassiveTeX -->
 <xsl:choose>
   <xsl:when test="$shade.verbatim != 0">

    <xsl:choose>
    <!-- if we are an ancestor of entry, we ignore the shaded flag -->
     <xsl:when test="ancestor::entry">
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
       xsl:use-attribute-sets="monospace.verbatim.properties shade.verbatim.style">
      <xsl:copy-of select="$content"/>
      </fo:block>
     </xsl:otherwise>
    </xsl:choose>
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

 <!-- customization header content -->

<xsl:template name="header.content">
  <xsl:param name="pageclass" select="''"/>
  <xsl:param name="sequence" select="''"/>
  <xsl:param name="position" select="''"/>
  <xsl:param name="gentext-key" select="''"/>
  
  <fo:block>
   
   <!-- sequence can be odd, even, first, blank -->
   <!-- position can be left, center, right -->
   <xsl:choose>
    <xsl:when test="$sequence = 'blank'">
     <!-- nothing -->
    </xsl:when>
    
    <xsl:when test="$position='left'">
        <!-- Same for odd, even, empty, and blank sequences -->
        <xsl:call-template name="draft.text"/>
    </xsl:when>
    
    <xsl:when test="($sequence='odd' or $sequence='even') and $position='center'">
     <xsl:if test="$pageclass != 'titlepage'">
      <xsl:choose>
       <xsl:when test="ancestor::book and ($double.sided != 0)">
         <fo:retrieve-marker retrieve-class-name="section.head.marker"
          retrieve-position="first-including-carryover"
          retrieve-boundary="page-sequence"/>
       </xsl:when>
       <xsl:otherwise>

         <!-- use Chapter %n title form of markup rather than abbrev  -->
         <xsl:apply-templates select="." mode="object.title.markup"/>
        <!-- <xsl:apply-templates select="." mode="titleabbrev.markup"/> -->
       </xsl:otherwise>
      </xsl:choose>
     </xsl:if>
    </xsl:when>

   <xsl:when test="$position='center'">
    <!-- nothing for empty and blank sequences -->
   </xsl:when>

   <xsl:when test="$position='right'">
    <!-- Same for odd, even, empty, and blank sequences -->
    <xsl:call-template name="draft.text"/>
   </xsl:when>

   <xsl:when test="$sequence = 'first'">
    <!-- nothing for first pages -->
   </xsl:when>

   <xsl:when test="$sequence = 'blank'">
    <!-- nothing for blank pages -->
   </xsl:when>
  </xsl:choose>
  </fo:block>
 </xsl:template>

 <xsl:template match="appendix">
  <xsl:variable name="id">
    <xsl:call-template name="object.id"/>
  </xsl:variable>

  <xsl:variable name="master-reference">
    <xsl:call-template name="select.pagemaster"/>
  </xsl:variable>


  <fo:page-sequence hyphenate="{$hyphenate}"
                    font-size="5pt"
                    master-reference="{$master-reference}">
    <xsl:attribute name="language">
      <xsl:call-template name="l10n.language"/>
    </xsl:attribute>
    <xsl:attribute name="format">
      <xsl:call-template name="page.number.format"/>
    </xsl:attribute>
    <xsl:choose>
      <xsl:when test="not(preceding::chapter
                          or preceding::appendix
                          or preceding::article
                          or preceding::dedication
                          or parent::part
                          or parent::reference)">
        <!-- if there is a preceding component or we're in a part, the -->
        <!-- page numbering will already be adjusted -->
        <xsl:attribute name="initial-page-number">1</xsl:attribute>
      </xsl:when>
      <xsl:when test="$double.sided != 0">
        <xsl:attribute name="initial-page-number">auto-odd</xsl:attribute>
      </xsl:when>
    </xsl:choose>

    <xsl:attribute name="hyphenation-character">
      <xsl:call-template name="gentext">
        <xsl:with-param name="key" select="'hyphenation-character'"/>
      </xsl:call-template>
    </xsl:attribute>
    <xsl:attribute name="hyphenation-push-character-count">
      <xsl:call-template name="gentext">
        <xsl:with-param name="key" select="'hyphenation-push-character-count'"/>
      </xsl:call-template>
    </xsl:attribute>
    <xsl:attribute name="hyphenation-remain-character-count">
      <xsl:call-template name="gentext">
        <xsl:with-param name="key" select="'hyphenation-remain-character-count'"/>
      </xsl:call-template>
    </xsl:attribute>

    <xsl:apply-templates select="." mode="running.head.mode">
      <xsl:with-param name="master-reference" select="$master-reference"/>
    </xsl:apply-templates>

    <xsl:apply-templates select="." mode="running.foot.mode">
      <xsl:with-param name="master-reference" select="$master-reference"/>
    </xsl:apply-templates>

    <fo:flow flow-name="xsl-region-body">
      <fo:block id="{$id}">
        <xsl:call-template name="appendix.titlepage"/>
      </fo:block>

      <xsl:variable name="toc.params">
        <xsl:call-template name="find.path.params">
          <xsl:with-param name="table" select="normalize-space($generate.toc)"/>
        </xsl:call-template>
      </xsl:variable>

      <xsl:if test="contains($toc.params, 'toc')">
        <xsl:call-template name="component.toc"/>
        <xsl:call-template name="component.toc.separator"/>
      </xsl:if>
      <xsl:apply-templates/>
    </fo:flow>
  </fo:page-sequence>
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
